import click


class HeaderKeyVal(click.ParamType):
    name = 'kv'

    def convert(self, value, param, ctx):
        try:
            if type(value) is str and len(value.split(":")) == 2:
                keyval = value.split(":")
                print(keyval)
                return(keyval[0], keyval[1])
            else:
                raise ValueError
        except ValueError:
            self.fail(f"{value} is an invalid format, use Key:Value format", param, ctx)
