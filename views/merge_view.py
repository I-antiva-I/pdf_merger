from typing import List

from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QWidget, QFileDialog

from components.merge.action_panel_component import ActionPanelComponent
from components.merge.control_panel_component import ControlPanelComponent
from components.merge.document_component import DocumentComponent
from components.merge.document_panel_component import DocumentPanelComponent
from interfaces.i_view import IViewMeta, IView
from managers.message_manager import MessageType, MessageManager
from viewmodels.merge_viewmodel import MergeViewModel, DocumentItem


class MergeView(QWidget, IView, metaclass=IViewMeta):
    def __init__(self, viewmodel: MergeViewModel):
        super().__init__()

        self.viewmodel = viewmodel

        self.control_panel = ControlPanelComponent()
        self.document_panel = DocumentPanelComponent()
        action_panel = ActionPanelComponent()

        self. control_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        layout.addWidget(self.control_panel)
        layout.addWidget(self.document_panel)
        layout.addWidget(action_panel)

        self.control_panel.button_add_file.clicked.connect(self.on_button_add_file_clicked)

        # Subscribe
        MessageManager.subscribe(MessageType.PDF_PATHS_SELECTED,
                                 self.viewmodel, self.viewmodel.on_pdf_paths_selected)

        MessageManager.subscribe(MessageType.ADD_DOCUMENT,
                                 self, self.add_document)

        MessageManager.subscribe(MessageType.MERGE_VIEW__DISPLAY_AS_GRID,
                                 self.document_panel, self.document_panel.display_as_grid)

        MessageManager.subscribe(MessageType.MERGE_VIEW__DISPLAY_AS_LIST,
                                 self.document_panel, self.document_panel.display_as_list)

        MessageManager.subscribe(MessageType.MERGE_VIEW__DOCUMENT_REMOVED,
                                 self.viewmodel, self.viewmodel.remove_document)

        MessageManager.subscribe(MessageType.DOCUMENT_REMOVE_CLICKED,
                                self, self.remove_document)

        MessageManager.subscribe(MessageType.ACTION_MERGE_CLICKED,
                                 self.viewmodel, self.viewmodel.merge_documents)

     #   MessageManager.subscribe(MessageType.DOCUMENT_REMOVE_CLICKED, self.viewmodel, self.viewmodel.remove_document)
      #  MessageManager.subscribe(MessageType.DOCUMENT_REMOVE_CLICKED, self, self.remove_document)
     #
     #
     #
       # MessageManager.subscribe(MessageType.REORDER, self.viewmodel, self.viewmodel.reorder_documents)

    @property
    def viewmodel(self) -> MergeViewModel:
        return self._viewmodel

    @viewmodel.setter
    def viewmodel(self, value: MergeViewModel):
        self._viewmodel = value

    def add_document(self, document_items: List[DocumentItem]):
        for document_item in document_items:
            self.document_panel.add_document_component(document_item)

        self.control_panel.set_number_of_documents(self.document_panel.number_of_inner_components)

    def remove_document(self, document_component: DocumentComponent):
        self.document_panel.remove_document_component(document_component)
        self.control_panel.set_number_of_documents(self.document_panel.number_of_inner_components)

    def on_button_add_file_clicked(self):
        pdf_paths: List[str]
        pdf_paths, restriction = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf)")

        if not pdf_paths:
            MessageManager.send(MessageType.PDF_PATHS_NONE_SELECTED)
        else:
            MessageManager.send(MessageType.PDF_PATHS_SELECTED, pdf_paths=pdf_paths)




    """
    def reindex_documents(self, deleted_index: int):
        for document_component in self.inner_components.values():
            print("D", document_component.document_index, deleted_index)
            if document_component.document_index > deleted_index:
                document_component.update_document_index(document_component.document_index-1)
     """













