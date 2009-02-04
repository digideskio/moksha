from tw.jquery.ui_tabs import JQueryUITabs
from tw.api import Widget
from pylons import config, request
from repoze.what import predicates
from moksha.lib.helpers import eval_app_config, ConfigWrapper

import urllib

class TabbedContainerTabs(Widget):
    template = 'mako:moksha.api.widgets.containers.templates.tabbedcontainer_tabs'

class TabbedContainerPanes(Widget):
    template = 'mako:moksha.api.widgets.containers.templates.tabbedcontainer_panes'

tabwidget = TabbedContainerTabs('tabs')
panewidget = TabbedContainerPanes('panes')

"""
:Name: TabbedContainer
:Type: Container
"""
class TabbedContainer(JQueryUITabs):
    """
    :tabs: An ordered list of application tabs to display
           Application descriptors come from the config wrappers in
           moksha.lib.helpers

           tabs can either be in serialized string format or as a list of
           config wrapper objects.  Using strings means you don't have to
           import the wrappers and predicates but can get unwieldy if there
           is a long list of wrappers

    :config_key: the configuration key used to store the serialized tab config
                 in a configuration file instead of embeding it in the widget

    :template: you must provide a template in order to get styling correct.  The
               default template has minimal functionality.  The documentation
               for jQuery.UI.Tabs can be found at http://ui.jquery.org.
               FIXME: Write a tutorial and provide helper widgets so
               creating a template becomes really easy.
    """
    css=[] # remove the default css
    template = 'mako:moksha.api.widgets.containers.templates.tabbedcontainer'
    config_key = None # if set load config
    tabs = ()

    def update_params(self, d):

        super(TabbedContainer, self).update_params(d)

        tabs = eval_app_config(config.get(self.config_key, "None"))
        if not tabs:
            if isinstance(self.tabs, str):
                tabs = eval_app_config(self.tabs)
            else:
                tabs = self.tabs

        # Filter out any None's in the list which signify apps which are
        # not allowed to run with the current session's authorization level
        tabs = ConfigWrapper.process_wrappers(tabs)
        d['tabs'] = tabs
        d['tabwidget'] = tabwidget
        d['panewidget'] = panewidget
        d['root_id'] = d['id']

