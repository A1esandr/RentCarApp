'''Пара функций для построения html кода ответа'''

def make_rows(data):
        result = ''
        count = 1
        for item in data:
            result += '<tr>'
            result += ('<td>'+str(count)+'</td>')
            for row in item:
                result += ('<td>'+str(row)+'</td>')
            result += '</tr>'
            count += 1
        return result

def make_options(data):
    result = ''
    for item in data:
        result += ('<option value="'+str(item[0])+'">'+item[1]+'</option>')
    return result
