__author__ = 'jaeyoung'


def make(url):
    tmp = dict()
    param_line = url.split("?")[1]
    param_list = param_line.split("&")
    for param in param_list:
        par = param.split("=")

        tmp[par[0]] = par[1]

    return tmp