class Tag:

    '''объекты класаа могут быть одиночным и парным, содержать классы
    и текст внутри себя'''

    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = []

        '''если атрибут klass указан
        записываем его в словарь self.attributes'''

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        '''перебераем словарь именованых аргументов
        если есть нижнее подчеркивание заменяем его на тире'''

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    '''наполняем список self.children'''

    def __iadd__(self, other):
        self.children.append(other)
        return self

    '''переводим полученный объект в сторку'''

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(' %s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        '''проверяем есть ли потомки, если есть записываем открывающий тэг
        проверяем есть ли текст и еще потомки
        записываем закрывающий тэг 
        если потомков нет проверяем нужен ли закрывающий тэг'''

        if self.children:
            opening = "<{tag}{attrs}>\n".format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>\n".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag}{attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )


class TopLevelTag(Tag):

    '''класс TopLevelTag наследует у класса Tag
    методы __iadd__, __enter__ и __exit__'''

    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __str__(self):
        html = "<%s>\n" % self.tag
        for child in self.children:
            html += str(child)
        html += "</%s>\n" % self.tag
        return html

class HTML(TopLevelTag):

    '''класс HTML наследует у TopLevelTag метод __str__
    для этого добавляем значение по умолчанию для self.tag
    методы __iadd__ и __enter__ как и TopLevelTag наследует
    у класса Tag'''

    def __init__(self, output=None):
        self.output = output
        self.children = []
        self.tag = "html"

    def __exit__(self, *args, **kwargs):
        '''если атрибут output указан открываем на запись файл
        с указаным в атрибуте именем'''
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)


def main(output=None):

    '''функция main принимает на вход один аргумент - имя файла
    для записи html кода, аргумент не обязательный'''

    '''создаем экземпляр класса HTML (только тэг)
    в него вкладываем тэг верхнего уровня head и тэг title с текстом hello'''

    with HTML(output=output) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        '''вклабываем в HTML тег body, с потомками'''

        with TopLevelTag("body") as body:

            '''h1 вложенный в body с указанием класса и текстом внутри'''

            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            '''div вложенный в body с указанием классов и id
            в него вложен параграф с текстом внутри'''

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                '''также внутрь div вложен тег img с необходимыми атрибумами,
                is_single=True говорит о том, что тэгне парный'''

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body


if __name__ == "__main__":
    main()