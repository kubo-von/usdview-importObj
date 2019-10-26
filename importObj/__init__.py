from pxr import Tf
from pxr.Usdviewq.plugin import PluginContainer



class importObjContainer(PluginContainer):

    def registerPlugins(self, plugRegistry, usdviewApi):

        importer = self.deferredImport(".importer")
        self._importObj = plugRegistry.registerCommandPlugin(
            "importObjContainer.printMessage",
            "Import .obj",
            importer.importObj)

    def configureView(self, plugRegistry, plugUIBuilder):

        importMenu = plugUIBuilder.findOrCreateMenu("Import")
        importMenu.addItem(self._importObj)

Tf.Type.Define(importObjContainer)