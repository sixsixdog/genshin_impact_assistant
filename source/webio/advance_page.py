from source.webio.page import Page
from source import webio
from source.webio import manager
from source.webio.util import *

class AdvancePage(Page):
    """Page的加强版，多了一个显示页面切换的功能

    Args:
        Page (_type_): _description_
    """

    DOCUMENT_DEFAULT_LINK = f"https://genshinimpactassistant.github.io/GIA-Document/#/{GLOBAL_LANG}/"

    def __init__(self, page_name="", document_link=''):
        super().__init__(page_name)
        if document_link == '':
            self.document_link = self.DOCUMENT_DEFAULT_LINK
        else:
            if GLOBAL_LANG not in document_link:
                document_link = document_link.replace("/#/", f"/#/{GLOBAL_LANG}/")
            self.document_link = document_link
    
    def _on_load(self):
        with output.use_scope(self.main_scope):
            # 标题
            if DEBUG_MODE:
                title = t2t('# GIA DEBUG') + f" {GIA_VERSION}"
            else:
                title = t2t('# GIA GUI') + f" {GIA_VERSION}"
            output.put_row([
                output.put_markdown(title)
            ])
            output.put_link(
                t2t('View a tutorial on this feature') if self.document_link != self.DOCUMENT_DEFAULT_LINK else t2t('View GIA Document'),
                url=self.document_link, new_window = True).style('font-size: 20px')
            # 页面切换按钮
            output.put_buttons(self._value_list2buttons_type(list(manager.page_dict)), onclick=webio.manager.load_page, scope=self.main_scope)
            super()._on_load()
        