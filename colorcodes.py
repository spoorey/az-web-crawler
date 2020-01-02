import math
def colorcode_by_argv(argv, articlesCount, maxArticlesPerKey):
    if argv == 'sqrt':
        return colorcode_sqrt(articlesCount, maxArticlesPerKey)
    elif argv == 'blue':
        return colorcode_blue(articlesCount, maxArticlesPerKey)
    return colorcode_default(articlesCount, maxArticlesPerKey)

def colorcode_sqrt(articlesCount, maxArticlesPerKey):
    relation = math.sqrt(articlesCount)/math.sqrt(maxArticlesPerKey)
    if (relation > 0.5):
        red = '00'
        green = (relation-0.5)*2*int('ff',16)
        green = format(int(green), 'X')
        green = green.rjust(2, '0')
    else:
        green = '00'
        red = (relation)*2*int('ff',16)
        red = int('ff', 16)-red
        red = format(int(red), 'X')
        red = red.rjust(2, '0')
    return red + 'FF' + green 
def colorcode_default(articlesCount, maxArticlesPerKey):
    relation = articlesCount/maxArticlesPerKey
    if (relation > 0.5):
        red = '00'
        green = (relation-0.5)*2*int('ff',16)
        green = format(int(green), 'X')
        green = green.rjust(2, '0')
    else:
        green = '00'
        red = (relation)*2*int('ff',16)
        red = int('ff', 16)-red
        red = format(int(red), 'X')
        red = red.rjust(2, '0')
    return red + 'FF' + green
def colorcode_blue(articlesCount, maxArticlesPerKey):
    relation = articlesCount/maxArticlesPerKey
    color = relation*int('ff', 16)
    color = int('ff', 16)-color
    color = format(int(color), 'X')
    color = color.rjust(2, '0')

    return color + color + 'FF'
