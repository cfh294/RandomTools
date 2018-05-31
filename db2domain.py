import cx_Oracle
import argparse


class Column(object):

    type_conversion = {
        "VARCHAR2":         "String",
        "VARCHAR":          "String",
        "LONG":             "int",
        "NUMBER":           "int",
        "FLOAT":            "float",
        "INT":              "int",
        "INTEGER":          "int",
        "DECIMAL":          "float",
        "DOUBLE PRECISION": "double",
        "DATE":             "Date",
        "TIMESTAMP":        "Date"
    }

    def __init__(self, name, nullable, data_type, data_length, precision, chop_prefix=None):

        stripped_type = data_type.split("(")[0]
        self.old_name = name
        self.name = underscore_to_camelcase(name, prefix=chop_prefix)
        self.nullable = "true" if nullable == "Y" else "false"
        self.data_type = self.get_type(stripped_type, precision)
        self.data_length = data_length
        self.precision = precision
        self.mapping = "\t\t\t{0} column: '{1}'\n".format(self.name, self.old_name.upper())

    def get_type(self, in_data_type, in_precision):

        found_type = self.type_conversion[in_data_type]
        if in_data_type == "NUMBER" and in_precision == 1:
            return "boolean"
        else:
            return found_type


def underscore_to_camelcase(value, prefix=None):
    """
    Solution found at:
    https://stackoverflow.com/questions/4303492/how-can-i-simplify-this-conversion-from-underscore-to-camelcase-in-python
    :param value:
    :param prefix:
    :return:
    """
    def camelcase():
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()

    if prefix is not None:
        value = value.replace(prefix, "", 1)
        value = value[1:] if value[0] == "_" else value

    return "".join(next(c)(x) if x else '_' for x in value.split("_"))


def get_column_list(in_cursor, in_owner, in_table):
    sql = "select lower(column_name) from all_tab_columns where upper(owner)=:in_table_owner and " \
          "upper(table_name)=:in_table_name"
    parameters = {"in_table_owner": in_owner.upper(), "in_table_name": in_table.upper()}
    in_cursor.execute(sql, parameters)
    return [result[0] for result in in_cursor.fetchall()]


def get_column_object(in_cursor, in_owner, in_table, in_column, chop_prefix=None):

    sql = "select lower(column_name), nullable, data_type, data_length, data_precision " \
          "from all_tab_columns where upper(table_name)=:in_table_name and " \
          "upper(column_name)=:in_column_name and upper(owner)=:in_table_owner"
    parameters = {"in_table_name": in_table.upper(), "in_column_name": in_column.upper(),
                  "in_table_owner": in_owner.upper()}
    in_cursor.execute(sql, parameters)
    data = in_cursor.fetchall()
    if len(data) > 0:
        data = data[0]
        return Column(data[0], data[1], data[2], data[3], data[4], chop_prefix)
    else:
        return None


def parse_connection(login, password):

    # ex) user@//host:port/service_name
    login_parts = login.split("@")
    user, server = login_parts[0], login_parts[1]

    # split the port and the host, strip the leading "//"
    server_parts = server.split(":")
    host = server_parts[0].replace("//", "")

    # parse out the service name, create the dsn string
    port_and_service_name = server_parts[1].split("/")
    port, service_name = port_and_service_name[0], port_and_service_name[1]

    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    return cx_Oracle.connect(user=user, password=password, dsn=dsn)


def get_arg_parser():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("connection", help="An Oracle jdbc connection string.")
    parser.add_argument("password", help="A password for the given Oracle connection.")
    parser.add_argument("domain", help="The desired name of the domain class.")
    parser.add_argument("owner", help="The owner of the table.")
    parser.add_argument("table", help="The name of the table.")

    parser.add_argument("-vf", "--version", type=str, help="The name of the version field.", default=None)
    parser.add_argument("-i", "--id", type=str,  help="The name of the grails-friendly id field.", default=None)
    parser.add_argument("-pf", "--prefix", type=str, help="The column prefix to be removed.", default=None)
    return parser


if __name__ == "__main__":

    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
    owner, table = args.owner, args.table
    class_name = args.domain
    id_column = args.id
    version_column = args.version
    in_chop_prefix = args.prefix

    with parse_connection(args.connection, args.password) as connection:

        cursor = connection.cursor()
        column_list = get_column_list(cursor, owner, table)
        groovy_file = "class " + class_name + " {\n\n"
        constraints = "\tstatic constraints = {\n\n"
        mapping = "\tstatic mapping = {{\n\n\t\t\ttable '{0}.{1}'\n".format(owner.upper(), table.upper())

        if id_column is not None:
            mapping += "\t\t\tid column: '{0}', name: 'id'\n".format(id_column.upper())
            groovy_file += "\t// The unique id field\n\tint id\n\n"
            column_list.remove(id_column)

        if version_column is not None:
            groovy_file += "\t// The version field\n\tint version\n\n"
            mapping += "\t\t\tversion column: '{0}', name: 'version'\n\n".format(version_column.upper())
            column_list.remove(version_column)
        else:
            mapping += "\t\t\tversion false\n"

        groovy_file += "\t// All other fields\n"
        ordered_fields = []
        for column_name in column_list:
            column_object = get_column_object(cursor, owner, table, column_name, chop_prefix=in_chop_prefix)
            ordered_fields.append("\t{0} {1}\n".format(column_object.data_type, column_object.name))
            constraints += "\t\t\t{0}(nullable:{1})\n".format(column_object.name, column_object.nullable)

            if in_chop_prefix is not None:
                mapping += column_object.mapping
        cursor.close()
        del cursor

        groovy_file += "".join(sorted(ordered_fields))

        mapping += "\t}\n\n"
        constraints += "\t}"
        groovy_file += "\n" + mapping + constraints + "\n}"

        print(groovy_file)
