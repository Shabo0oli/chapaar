from django import template

register = template.Library()

@register.filter(name='checkinlist')
def checkinlist(value, arg):
    reslist= []
    for c  in value :
        flag = 0
        for a , b in arg :
            if int(a.CourseName.id) == int(c['id']) :
                flag = 1
                break
        if flag==0 :
            reslist.append(c)


    return reslist
