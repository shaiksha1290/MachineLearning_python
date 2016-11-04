import inspect, re, sys;
# search the stack from the top to the bottom for first py file (THIS) file:
for i in inspect.stack():
   path = re.search("^(.*)[\\\/]([a-zA-Z0-9_]*\.py)", i[1], re.I)
   if path:
      base_path = path.groups()[0]
      break;
   # end if
# end if
import os
base_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
if base_path.endswith('/'):
   base_path = base_path[:-1] # remove last char
# end if
sys.path.insert(0,base_path + '/lib_non_tpip');  # for pygtk
sys.path.insert(0,base_path + '/include');       # for sql_interface
sys.path.insert(0,base_path + '/tldb_tools');    # for copy_results_to_tldb
import os
os.chdir(base_path) # so that the .glade file can be found
import time

try:  # this is all in a try statement to help with capturing import issues and being able to actually solve them...
   import sql_interface
   import test_event_import
   import pygtk
   pygtk.require('2.0')
   import gtk
   import gtk.glade
   import gobject
   import urllib
   import os

   try:
      import webbrowser
   except:
      self._print("Link does not work")
   #end try
   _URI_LIST = 80
   targets = [ ( 'text/uri-list', 0, _URI_LIST ) ]
   
   def get_file_path_from_uri(uri):
      path = ""
      if uri.startswith('file:////'):
         path = uri[7:]
      elif uri.startswith('file:\\\\\\') or uri.startswith('file:///'):
         path = uri[8:]
      elif uri.startswith('file://'):
         path = uri[7:]
      elif uri.startswith('file:'):
         path = uri[5:]
      # end if
      
      # TODO: what to do about spaces in filenames?
      path = urllib.url2pathname(path) # escape special chars
      path = path.strip('\r\n\x00')
      return path
   # end if
      
   class UpdateTestEventGUI:
      """This is a GTK application"""
      
      def __init__( self , glade_file = "update_test_event.glade"):
         self.wTree = gtk.glade.XML(glade_file)
         self.gtk = gtk
         self.window = self.wTree.get_widget("windowMain")
      
         if self.window:
            self.window.connect("destroy", gtk.main_quit)
            self.window.set_title("Test Event Management Tool")
         # end if
         
         #Set all widgets from glade GUI
         self.switchfam = self.wTree.get_widget("switchfam")
         self.connection = self.wTree.get_widget("connection_label")
         self.program_combo = self.wTree.get_widget("program")
         self.test_event_combo = self.wTree.get_widget("test_event_combo")
         #Update Test Case Tab widgets
         self.page_notebook = self.wTree.get_widget("tab_notebook")
         self.test_case_file_chooser = self.wTree.get_widget("test_case_file_chooser")
         self.assignments_file_chooser = self.wTree.get_widget("assignments_file_chooser")
         self.purge_extras_checkbox = self.wTree.get_widget("purge_extras")
         self.default_rerun_state_checkbox = self.wTree.get_widget('default_rerun_state_checkbox')
         self.default_rerun_state_checkbox1 = self.wTree.get_widget('default_rerun_state_checkbox1')
         self.btnUpdateTestCases = self.wTree.get_widget("buttonUpdateTestCases")
         self.btnUpdateAssignments = self.wTree.get_widget("buttonUpdateAssignments")
         #Add/Edit Test Event Info Tab widgets
         self.test_event_name_string =self.wTree.get_widget("test_event_name_string")
         self.test_event_build_string =self.wTree.get_widget("test_event_build_string")
         self.svn_repository_url_string =self.wTree.get_widget("svn_repository_url_string")
         self.test_event_starting_build_string =self.wTree.get_widget("test_event_starting_build_string")
         self.test_event_latest_build_string =self.wTree.get_widget("test_event_latest_build_string")
         self.calendar_select = self.wTree.get_widget("Calendar_Select")
         self.start_date_entry = self.wTree.get_widget("start_date_entry")
         self.end_date_entry = self.wTree.get_widget("end_date_entry")
         self.calendar_select2 = self.wTree.get_widget("Calendar_Select_2")
         self.debug_checkbox = self.wTree.get_widget("debug")
         self.formal_checkbox = self.wTree.get_widget("formal")
         self.burndown_checkbox = self.wTree.get_widget("burndown")
         self.has_multiple_aircraft_types_checkbox = self.wTree.get_widget("has_multiple_aircraft_types")
         self.btnUpdateTestEvent = self.wTree.get_widget("buttonUpdateTestEvent")
         self.manage_assets_button = self.wTree.get_widget("manage_assets_button")
         #copy tab widgets
         self.copy_test_event_combo = self.wTree.get_widget("copy_to_test_event_combo")
         self.btnCopyEvent = self.wTree.get_widget("copy_test_case_to_event")
         #Assets tab widgets
         self.assets_page = self.wTree.get_widget("Asset_Page")
         self.assets_tab = self.wTree.get_widget("Assets_Tab")
         self.test_event_assets = self.wTree.get_widget("assets_in_event")
         self.available_assets = self.wTree.get_widget("available_assets_list")
         self.add_button = self.wTree.get_widget("add_button")
         self.remove_button = self.wTree.get_widget("remove_button")
         self.assets_in_label = self.wTree.get_widget("Assets_in_label")
         self.clear_list_btn = self.wTree.get_widget("clear_list")
         self.create_asset = self.wTree.get_widget("create_asset")
         #bottom main GUI widgets
         self.text_view = self.wTree.get_widget("textview_output")
         self.linkbutton = self.wTree.get_widget("linkbutton")
         self.buttonQuit = self.wTree.get_widget("buttonQuit")
         #Calendar window widgets
         self.calendar_window = self.wTree.get_widget("calendar_popup")
         self.cal_widget = self.wTree.get_widget("calendar_widget")
         self.cal_cancel = self.wTree.get_widget("calendar_cancel")
         #Progress Pop-Up widgets
         self.progress_bar = self.wTree.get_widget("progress_bar")
         self.progress_window = self.wTree.get_widget("progress_popup")
         self.process_cancel = self.wTree.get_widget('process_cancel')
         #Test Asset Edit Pop-Up
         self.test_asset_window = self.wTree.get_widget("test_asset_popup")
         self.test_asset_button = self.wTree.get_widget("change_asset_button")
         self.asset_id_label = self.wTree.get_widget("test_asset_id_label")
         self.asset_nickname_entry = self.wTree.get_widget("nickname_entry")
         self.asset_machname_entry = self.wTree.get_widget("machine_name_entry")
         self.num_cdus_entry = self.wTree.get_widget("number_cdus")
         self.cdu_power_entry = self.wTree.get_widget("cdu_power")
         #Warning Pop-Up
         self.warning_window = self.wTree.get_widget("warning_popup")
         self.warning_message = self.wTree.get_widget("warning_text")
         #Sync tab widgets
         self.tldb_program_combo = self.wTree.get_widget("tldb_program_combo")
         self.tldb_event_combo = self.wTree.get_widget("tldb_test_event_combo")
         self.tldb_description_combo = self.wTree.get_widget("tldb_description_combo")

         
         #set checkbox values and their active states         
         self.purge_extras = True
         self.purge_extras_checkbox.set_active(self.purge_extras)
         self.default_rerun_state = True
         self.default_rerun_state_checkbox.set_active(self.default_rerun_state)
         self.default_rerun_state_checkbox1.set_active(self.default_rerun_state)
         self.debug = False
         self.debug_checkbox.set_active(self.debug)
         self.formal = None
         self.formal_state = False
         self.formal_checkbox.set_active(self.formal_state)
         self.burndown = None
         self.burndown_state = True #set default to always have a burndown plot
         self.burndown_checkbox.set_active(self.burndown_state)
         
         #set up drag drop capabilities for file choosers
         self.test_case_file_chooser.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
                          gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
                          targets, gtk.gdk.ACTION_COPY)
         self.assignments_file_chooser.drag_dest_set( gtk.DEST_DEFAULT_MOTION |
                          gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
                          targets, gtk.gdk.ACTION_COPY)
         #stuff for test case/assignments file handling
         filter = gtk.FileFilter()
         filter.set_name("CSV Files")
         filter.add_pattern("*.csv")
         all_files = gtk.FileFilter()
         all_files.set_name("All Files")
         all_files.add_pattern("*")
         self.test_case_file_chooser.add_filter(filter)
         self.test_case_file_chooser.add_filter(all_files)
         self.assignments_file_chooser.add_filter(filter)
         self.assignments_file_chooser.add_filter(all_files)
         #date formatting
         self.display_format = "%m-%d-%Y"
         self.sql_date_format = "%Y-%m-%d"
         # Set up defaults for things that will be defined later
         self.selected_program_name = None
         self.selected_program_id = None
         self.selected_test_event_id = None
         self.test_case_file = None
         self.assignments_file = None
         self.external_link = None
         # second tab
         self.selected_test_event_name = None
         self.start_date = None
         self.end_date = None
         self.selected_test_event_build = None
         self.selected_test_event_starting_build = None
         self.selected_test_event_latest_build = None
         self.has_multiple_aircraft_types = None
         self.has_multiple_aircraft_types_state = False
         self.selected_svn_repository_url = None
         # set up dictionary of signals and associated actions
         dic = { 
            "on_buttonQuit_clicked" : self.quit,
            "on_windowMain_destroy" : self.quit,
            "on_logout/switchfam_clicked" : self.switch_family,
            "on_program_changed" : self.program_combo_callback,
            "on_test_event_changed" : self.test_event_combo_callback,
            "on_assignments_file_chooser_drag_data_received" : self.file_drop,
            "on_test_case_file_chooser_drag_data_received" : self.file_drop,
            "on_assignments_file_chooser_selection_changed" : self.get_assignments_file,
            "on_test_case_file_chooser_selection_changed" : self.get_test_case_file,
            "on_purge_extras_toggled" : self.get_purge_extras_state,
            "on_default_rerun_toggled" : self.get_default_rerun_state,
            "on_buttonUpdate_clicked" : self.update,
            "on_buttonUpdateAssignments_clicked" : self.update,
            "on_has_multiple_aircraft_types_toggled" : self.get_has_multiple_aircraft_types_state,
            "on_debug_toggled" : self.get_debug_state,
            "on_buttonUpdateTestEvent_clicked" : self.update_test_events,
            "on_copy_test_case_to_event_clicked" : self.copy_test_cases,
            "on_copy_test_case_to_event_keep_results_clicked" : self.copy_test_cases_keep_results,
            "on_linkbutton_clicked" : self.linkbutton_callback,
            "on_Calendar_Select_clicked" : self.on_Calendar_Select_clicked,
            "on_Calendar_Select_2_clicked" : self.on_Calendar_Select_clicked,
            "on_copy_to_test_event_combo_changed" : self.copy_test_event_combo_callback,
            "on_burndown_toggled" : self.get_burndown_state,
            "on_formal_toggled" : self.get_formal_state, 
            "on_calendar_widget_day_selected_double_click" : self.calendar_widget_day_selected_double_click,
            "on_calendar_cancel_clicked" : self.on_calendar_cancel_clicked,            
            'on_end_date_entry_focus_out_event' : self.date_format,
            'on_start_date_entry_focus_out_event' : self.date_format,
            "on_process_cancel_clicked" : self.on_cancel,
            "on_add_button_clicked" : self.add_asset,
            "on_remove_button_clicked" : self.remove_asset,
            "on_clear_list_clicked" : self.clear_list,
            "on_create_asset_clicked" : self.show_asset_edit,
            "on_asset_cancel_clicked" : self.asset_edit_cancel,
            "on_change_asset_button_clicked" : self.change_assets,
            "on_manage_assets_button_clicked" : self.to_asset_management,
            "on_Edit_Asset_btn_clicked" : self.show_asset_edit,
            "on_available_assets_list_cursor_changed" : self.select_test_asset,
            "on_assets_in_event_cursor_changed" : self.select_test_asset_in,
            "on_warning_ok_clicked" : self.warning_ok,
            "on_tldb_program_combo_changed" : self.tldb_program_callback,
            "on_tldb_test_event_combo_changed" : self.tldb_test_event_callback,
            "on_tldb_description_combo_changed" : self.tldb_description_callback,
            "on_Sync_button_clicked" : self.sync,
            "on_connect_tldb_clicked" : self.connect_tldb,
            "on_create_slist_button_clicked" : self.create_section_list,
            "on_export_section_list_to_tldb_button_clicked" : self.export_section_list_to_tldb,
         }
         #initialize objects for assets in test event treeview
         self.test_event_assets_tree_store = None
         self.asset_in_column = None
         assetNameCell = None
         self.test_event_assets.set_model(None)
         self.test_event_assets_tree_store = gtk.TreeStore(gobject.TYPE_STRING)
         self.asset_in_column = gtk.TreeViewColumn()
         assetNameCell = gtk.CellRendererText ()
         self.asset_in_column.pack_start(assetNameCell, True);
         self.test_event_assets.append_column(self.asset_in_column)
         self.asset_in_column.add_attribute (assetNameCell, "text", 0);

         #initialize objects for available assets treeview
         self.available_assets_tree_store = None
         asset_column = None
         assetNameCell = None
         self.available_assets.set_model(None)
         self.available_assets_tree_store = gtk.TreeStore(gobject.TYPE_STRING)
         asset_column = gtk.TreeViewColumn()
         asset_column.set_title("Available Test Assets")
         assetNameCell = gtk.CellRendererText ()
         asset_column.pack_start(assetNameCell, True);
         self.available_assets.append_column(asset_column)
         asset_column.add_attribute (assetNameCell, "text", 0);
         
         #default tldb values
         self.selected_tldb_description_id = None
         self.selected_tldb_event = None
         self.selected_tldb_program = None
         self.connected = False
         
         #default page numbers for certain tabs
         self.asset_page_num = 3
         self.notify_counter = 0
         self.sync_page_number = 4
         #set up signal connection between GUI and script
         self.wTree.signal_autoconnect( dic )
         self.default_to_page_num = 1
         self.initialized = False
         
      # end def
      
      def populate_program_list(self, widget=None):
         #based on selected family populate the program combo box
         self.selected_program_id = None
         self.selected_program_name = None
         self.programs_row_dict_array = sql_interface.Get_All_Programs()
         # set up the list of programs
         programs = gtk.ListStore(str)
         programs.append(["Choose a program..."])
         for row in self.programs_row_dict_array:
            item = row['program_name']
            programs.append([item])
         # end for
         self.program_combo.set_model(programs)
         # force "Choose a program..." to be selected
         self.program_combo.set_active(0)
      # end def
      
      def populate_test_event_list(self, widget=None):
         #determine test event list for program combo box selection
         program_index = self.program_combo.get_active()
         #initialize
         self.selected_test_event_build = None
         self.selected_test_event_starting_build = None
         self.selected_test_event_latest_build = None
         self.selected_test_event_id = None
         self.selected_test_event_name = None
         self.has_multiple_aircraft_types = None
         self.has_multiple_aircraft_types_state = False
         self.start_date = None
         self.end_date = None
         self.selected_svn_repository_url = None
         
         # set up the list of test_events
         test_events = gtk.ListStore(str)

         if self.selected_program_name is not None and program_index !=0:
            test_events.append(["Create or Choose a test event..."])
            self.test_events_row_dict_array = sql_interface.Get_All_Test_Events_For_This_Program(self.selected_program_id)
         
            for row in self.test_events_row_dict_array:
               item = "%s: %s"%(row['build'],row['test_event'])
               test_events.append([item])
            # end for
         else:
            test_events.append(["Choose a program first..."])
         # end if
         
         self.test_event_combo.set_model(test_events)
         self.copy_test_event_combo.set_model(test_events)
         
         # force "Choose a test event..." to be selected
         self.test_event_combo.set_active(0)
      # end def
      
      def populate_copy_test_event_list(self, index):
         #determine selection
         program_index = self.program_combo.get_active()
         # set up the list of copy test_events
         test_events = gtk.ListStore(str)
         if self.selected_program_name is not None and program_index != 0:
            test_events.append(["Choose a test event..."])
            self.copy_test_events_row_dict_array = list(sql_interface.Get_All_Test_Events_For_This_Program(self.selected_program_id))
            
            # since this is the copy event list, we don't want to include the source test event in the copy dropdown
            self.copy_test_events_row_dict_array.pop(index-len(test_events))
            
            #create list of available test events for copying
            for row in self.copy_test_events_row_dict_array:
               item = "%s: %s"%(row['build'],row['test_event'])
               test_events.append([item])
            # end for
         else:
            #unable to select a test event because no program is selected
            test_events.append(["Choose a program first..."])
         # end if not None
         self.copy_test_event_combo.set_model(test_events)
           
         # force "Choose a test event..." to be selected
         self.copy_test_event_combo.set_active(0)
            
      #end def
      
      def common_program_combo_callback(self, index):
         if index:
            #get data from selected program
            row = self.programs_row_dict_array[index-1]
            self.selected_program_name = row['program_name']
            self.selected_program_id = row['program_id']
            self._print('%s (%s) selected'%(self.selected_program_name,self.selected_program_id))
         else :
            self.selected_test_event_id = None
            self.selected_test_event_build = None
            self.selected_test_event_name = None
         # end if
      # end def

      def program_combo_callback(self, widget=None):
         if self.debug:
            self._print("program_combo_callback")
         #end if
         #determine active program and determine information 
         index = self.program_combo.get_active()
         self.common_program_combo_callback(index)
         #indicate to the user that since at this time no test event is selected you will create, not update, a test event from the add/edit tab
         self.btnUpdateTestEvent.set_label("Create Test Event")
         #fill test event combo with test events for this program
         self.populate_test_event_list()
         #end def
      # end def

      def common_test_event_combo_callback(self, index):
         if index:
            row = self.test_events_row_dict_array[index-1]
            self.selected_test_event_name = row['test_event']
            self.selected_test_event_build = row['build']
            self.selected_test_event_starting_build = row['starting_build']
            self.selected_test_event_latest_build = row['latest_build']
            self.selected_test_event_id = row['test_event_id']
            self.start_date = "%s"%row['start_date']
            self.end_date = "%s"%row['end_date']
            self.has_multiple_aircraft_types = row['has_multiple_aircraft_types']
            self.burndown = row['burndown_report']
            self.formal = row['formal']
            try:
               self.selected_svn_repository_url = row['log_file_repository_url']
            except:
               self.selected_svn_repository_url = None
            # end try
            
            #relate database tinyint values to the Boolean GUI states
            if self.formal == 0:
               self.formal_state = False
            else:
               self.formal_state = True
            #end if
            if self.burndown == 0:
               self.burndown_state = False
            else:
               self.burndown_state = True
            #end if
            if self.has_multiple_aircraft_types == 0:
               self.has_multiple_aircraft_types_state = False
            else:
               self.has_multiple_aircraft_types_state = True
            #end if
            self._print('%s: %s (%s) selected'%(self.selected_test_event_build,
                                                self.selected_test_event_name,
                                                self.selected_test_event_id))
         else :
            self.selected_test_event_id = None
            self.selected_test_event_build = None
            self.selected_test_event_starting_build = None
            self.selected_test_event_latest_build = None
            self.selected_test_event_name = None
            self.start_date = None
            self.end_date = None
            self.formal_state = False
            self.burndown_state = True # set the default burndown plot setting to True
            # Once a program is selected, the default assumption will be that
            # all test events will NOT have multiple aircraft types (this coincides
            # with the default which is captured in the database as well)
            self.has_multiple_aircraft_types_state = False
            self.selected_svn_repository_url = None

         # end if
      # end common_test_event_combo_callback

      def test_event_combo_callback(self, widget=None):
         if self.debug:
            self._print("test_event_combo_callback")
         #end if
         index = self.test_event_combo.get_active()

         #if changing from a test event that has assets to be managed, default to the add/edit tab to select formal state for new test event
         #because the newly selected event may not have the ability to manage assets, so we don't want to leave the user on a non-existent tab
         if self.page_notebook.get_current_page() == self.asset_page_num:
            self.default_to_page()
         #end if

         #get info for the selected test event
         self.common_test_event_combo_callback(index)
         #display this information in the GUI
         self.populate_build_and_name()
         #change button label on add/edit tab to give the user more clarity about the action that will take place upon click
         if index != 0:
            self.btnUpdateTestEvent.set_label("Update Test Event Info")
         else:
            self.btnUpdateTestEvent.set_label("Create Test Event")
         #end if
         #determine link to be displayed and accessible for the selected test event
         self.external_link = "https://%(server)s/STARWARS/test_event_status.php?test_family_id=%(family_id)s&test_event_id=%(test_event_id)s"%{
               'server': sql_interface.TEST_DATA_DB_CONN.server,
               'family_id':sql_interface.TEST_DATA_DB_CONN.family_id,
               'test_event_id': self.selected_test_event_id,
         }
         self.linkbutton.set_label(self.external_link)
         #change copy test event list according so that the selected test event will not be displayed for copying
         self.populate_copy_test_event_list(index)
      # end def

      def common_copy_test_event_combo_callback(self, index):
         #get information for the selected test event to be copied to
         if index:
            row = self.copy_test_events_row_dict_array[index-1]
            self.selected_copy_test_event_name = row['test_event']
            self.selected_copy_test_event_build = row['build']
            self.selected_copy_test_event_id = row['test_event_id']
            self._print('%s: %s (%s) selected'%(self.selected_copy_test_event_build,
                                                self.selected_copy_test_event_name,
                                                self.selected_copy_test_event_id))
         else :
            self.selected_copy_test_event_id = None
            self.selected_copy_test_event_build = None
            self.selected_copy_test_event_name = None
         # end if
      # end common_test_event_combo_callback

      def copy_test_event_combo_callback(self, widget=None):
         if self.debug:
            self._print("copy_test_event_combo_callback")
         #end if
         #determine the event which will have its contents modified by the copy action
         index = self.copy_test_event_combo.get_active()
         self.common_copy_test_event_combo_callback(index)
      # end def      
      
      def file_drop(self, widget, context, x, y, selection, target_type, timestamp):
         #determine file path 
         files = []
         if target_type in [_URI_LIST]:
            uri = selection.data.strip('\r\n\x00')
            uris = uri.split()
            for uri in uris:
               path = get_file_path_from_uri(uri)
               files.append(path)
            # end for
         # end for 
         if len(files) > 0:
            try:
               widget.set_filename(files[0])
            except:
               self._print("Unable to set filename.")
            # end try
         # else do nothing.
         # end if
      # end def
      
      def get_file(self, widget):
         return widget.get_filename()
      # end def
      
      def get_test_case_file(self, widget):
         self.test_case_file = self.get_file(widget)
      # end def
      
      def get_assignments_file(self, widget):
         self.assignments_file = self.get_file(widget)
      # end def
      
      def get_purge_extras_state(self, widget):
         self.purge_extras = widget.get_active()
      # end def
      
      def get_default_rerun_state(self, widget):
         self.default_rerun_state = widget.get_active()
         # keep things in sync throughout the gui
         if self.debug: self._print("get_default_rerun_state")
         self.default_rerun_state_checkbox.set_active(self.default_rerun_state)
         self.default_rerun_state_checkbox1.set_active(self.default_rerun_state)
      # end def
      
      def get_has_multiple_aircraft_types_state(self, widget):
         self.has_multiple_aircraft_types_state = widget.get_active()
         #differentiate between the state and actual database stored tinyint
         if self.has_multiple_aircraft_types_state is True:
            self.has_multiple_aircraft_types = 1
         else:
            self.has_multiple_aircraft_types = 0
         #end
      # end def
      
      def get_formal_state(self, widget = None):
         self.formal_state = widget.get_active()
         #differentiate between boolean GUI value and database required tinyint
         if self.formal_state == True:
            self.formal = 1
         elif self.formal_state == False:
            self.formal = 0
         #end if
         #test asset management only needed if test event is formal
         if self.formal_state is True and self.selected_test_event_id is not None:
            self.assets_page.show()
            self.manage_assets_button.show()
            self.populate_assets_available_list()
            self.populate_assets_in_event()
         else:
            self.assets_page.hide()
            self.manage_assets_button.hide()
         #end if
      # end def
      
      def get_burndown_state(self, widget):
         self.burndown_state = widget.get_active()
         #differentiate between boolean GUI value and database required tinyint
         if self.burndown_state == True:
            self.burndown = 1
         elif self.burndown_state == False:
            self.burndown = 0
         #end if
      # end def
      
      def get_debug_state(self, widget):
         self.debug = widget.get_active()
      # end def
      
      def populate_build_and_name(self, widget = None): # And all other test event info...
         #display all relevant test event information in the GUI for editing, etc.
         if self.debug:
            self._print("populate_build_and_name")
         #end if
         if self.selected_test_event_name is not None :
            if self.debug: self._print("Selected Test Event: %s"%str(self.selected_test_event_name))
            self.test_event_name_string.set_text(self.selected_test_event_name)
         else :
            self.test_event_name_string.set_text("")
         # end if
         
         if self.selected_test_event_build is not None :
            if self.debug: self._print("Build: %s"%str(self.selected_test_event_build))
            self.test_event_build_string.set_text(self.selected_test_event_build)
         else :
            self.test_event_build_string.set_text("")
         # end if
         
         if self.selected_svn_repository_url is not None :
            if self.debug: self._print("SVN Log File URL: %s"%str(self.selected_svn_repository_url))
            self.svn_repository_url_string.set_text(self.selected_svn_repository_url)
         else :
            self.svn_repository_url_string.set_text("")
         # end if
         
         if self.selected_test_event_starting_build is not None :
            if self.debug: self._print("Starting Build: %s"%str(self.selected_test_event_starting_build))
            self.test_event_starting_build_string.set_text(self.selected_test_event_starting_build)
         else :
            self.test_event_starting_build_string.set_text("")
         # end if
         
         if self.selected_test_event_latest_build is not None :
            if self.debug: self._print("Current Build: %s"%str(self.selected_test_event_latest_build))
            self.test_event_latest_build_string.set_text(self.selected_test_event_latest_build)
         else :
            self.test_event_latest_build_string.set_text("")
         # end if
         
         if self.start_date is not None :
            if self.debug: self._print("Start Date: %s"%str(self.start_date))
            self.start_date_entry.set_text(time.strftime(self.display_format,time.strptime(self.start_date,self.sql_date_format)))
         else :
            self.start_date_entry.set_text("")
         # end if
         if self.end_date is not None :
            if self.debug: self._print("End Date: %s"%str(self.end_date))
            self.end_date_entry.set_text(time.strftime(self.display_format,time.strptime(self.end_date,self.sql_date_format)))
         else :
            self.end_date_entry.set_text("")
         # end if
         if self.has_multiple_aircraft_types_state is not None :
            if self.debug: self._print("Has Multiple Aircraft Types is %s"%str(self.has_multiple_aircraft_types_state))
            self.has_multiple_aircraft_types_checkbox.set_active(self.has_multiple_aircraft_types_state)
         # end if
         if self.formal_state is not None :
            if self.debug: self._print("Formal is %s"%str(self.formal_state))
            self.formal_checkbox.set_active(self.formal_state)
         # end if

         if self.burndown_state is not None :
            if self.debug: self._print("Burndown is %s"%str(self.burndown_state))
            self.burndown_checkbox.set_active(self.burndown_state)
         # end if

         
      # end def  populate_build_and_name
      
      def _print(self, text):
         #handle the displaying of statements to the GUI textview
         textbuffer = self.wTree.get_widget("textview_output").get_buffer()
         current_text = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter())
         textbuffer.set_text("%s\n%s"%(current_text,text))
         #set view at end of inserted text
         self.text_view.scroll_to_mark(textbuffer.get_insert(),0)
      # end def
         
      def update(self, widget):
         if self.selected_test_event_id:
            #callback to update test event with new test cases from file and/or new assignments from file
            if self.debug:
               self._print("Debug is %s"%self.debug)
               self._print("Update")
               self._print("Selected Test Case File: %s"%self.test_case_file)
               self._print("Selected Assignments File: %s"%self.assignments_file)
            #end if
            self._print("Updating Test Event ID: %s"%self.selected_test_event_id)
            self._print("Purge Extras is %s"%self.purge_extras)
            
            if widget == self.btnUpdateAssignments:
               if self.assignments_file:
                  self.show_progress(update_what="Assignments")
                  test_event_import.process_assignments_file(assignments_file = self.assignments_file,
                                                             test_event_id = self.selected_test_event_id,
                                                             db_conn = sql_interface.TEST_DATA_DB_CONN,
                                                             gui_handle = self)
               else:
                  self._warning("You need to select an assignments file")
            else:
               if self.test_case_file:
                  self.show_progress(update_what="Test Cases")
                  self.cancelled = test_event_import.process_test_case_file(test_cases_file = self.test_case_file,
                                                           test_event_id = self.selected_test_event_id, 
                                                           purge_extras = self.purge_extras,
                                                           db_conn = sql_interface.TEST_DATA_DB_CONN,
                                                           gui_handle = self,
                                                           rerun_state = self.default_rerun_state) 
                  if self.assignments_file and self.cancelled is False:
                     self.show_progress(update_what="Assignments")
                     #end if
                     test_event_import.process_assignments_file(assignments_file = self.assignments_file,
                                                             test_event_id = self.selected_test_event_id,
                                                             db_conn = sql_interface.TEST_DATA_DB_CONN,
                                                             gui_handle = self)
                  #end if
               else:
                  self._warning("You need to select a test case file")
               #end if
            #end if
         else:
            self._warning("You need to select a test event to update")
      # end def
      
      def confirmed(self, message):
         """This function will pop up a modal confirmation dialog box and return
         True or False based on the user's response to the message provided."""
         # TODO: add confirmation dialog here...
         
         dialog = gtk.MessageDialog(
                        parent=None, 
                        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        type=gtk.MESSAGE_WARNING,
                        message_format=message)
         dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
         dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
         response = dialog.run()
         dialog.destroy()
                  
         return response == gtk.RESPONSE_OK
      # end if
      
      def copy_test_cases(self, widget = None):
         #callback to delete and then copy test case list and information from one event to another
         if self.debug:
            self._print("copy_test_cases")
            self._print("Debug is %s"%self.debug)
         #end if

         if self.selected_copy_test_event_id:
            if self.confirmed("Warning: This will DELETE all progress in this 'Copy To' event and mark everything to be [re]run."):
               self._print("Deleting and Copying Test Cases for Test Event ID: %s to selected Test Event ID: \t%s"%(self.selected_test_event_id,self.selected_copy_test_event_id))
               test_event_import.Copy_Test_Case_List_To_Test_Event(from_test_event = self.selected_test_event_id,
                                                                   to_test_event = self.selected_copy_test_event_id,
                                                                   db_conn = sql_interface.TEST_DATA_DB_CONN, gui_handle = self)
            # end if we really meant to do this
         else:
            self._warning("You need to select a test event to copy to")
         #end if
      # end def
      
      def copy_test_cases_keep_results(self, widget = None):
         #callback to copy test case list and information from one event to another
         if self.debug:
            self._print("copy_test_cases_keep_results")
            self._print("Debug is %s"%self.debug)
         #end if
         if self.selected_copy_test_event_id:
            if self.confirmed("Warning:\nThis will remove test cases from the 'Copy To' event which are not in the source test event.\n\n"+\
                  "Test cases which are not in the 'Copy To' event will be assigned to the same engineer as the source event with rerun state set according to the checkbox.\n\n"+\
                  "Test cases which exist in both events will remain unchanged (assignments, results, rerun state)."):
   
               self._print("Copying Test Cases for Test Event ID: %s to selected Test Event ID: \t%s"%(self.selected_test_event_id,self.selected_copy_test_event_id))
               test_event_import.Copy_Test_Case_List_To_Test_Event_Keep_Results(
                         from_test_event = self.selected_test_event_id,
                         to_test_event = self.selected_copy_test_event_id,
                         rerun_state = self.default_rerun_state,
                         db_conn = sql_interface.TEST_DATA_DB_CONN,
                         gui_handle = self)
            # end if
         else:
            self._warning("You need to select a test event to copy to")
         #end if
      # end def
      
      def update_test_events(self, widget = None):
         #callback to update or create a test event defined by the information provided for the GUI add/edit tab
         if self.debug:
            self._print("update_test_events")
         #end if
         build = self.test_event_build_string.get_text()
         name = self.test_event_name_string.get_text()
         starting_build = self.test_event_starting_build_string.get_text()
         latest_build = self.test_event_latest_build_string.get_text()
         self._print("\nUpdate or Create Test Event")
         self._print("Test Event ID: %s"%self.selected_test_event_id)
         self._print("Name: %s"%name)
         self._print("Build: %s"%build)
         self._print("Starting Build: %s"%starting_build)
         self._print("Latest Build: %s"%name)
         self._print("Has Multiple Aircraft Types: %s\n"%self.has_multiple_aircraft_types_state)
         svn_log_file_url = self.svn_repository_url_string.get_text()
         self._print("SVN Log File URL: %s"%svn_log_file_url)

         query = """
            select
               count(*) as count 
            from
               test_events
            where
               test_event = '%s'
               and program_id = '%s'
            """%(name, self.selected_program_id)
         if self.selected_test_event_id is not None:
            query += "and test_event_id != '%s'"%self.selected_test_event_id
         # end if
         count = sql_interface.Execute(query,
            db_conn = sql_interface.TEST_DATA_DB_CONN).fetchall()[0]['count']
         test_event_name_is_unique = count == 0
         
         if test_event_name_is_unique or \
               self.confirmed("A test event with the name '%s' already exists for this program.  This could be confusing, is it OK to reuse this test event name?"%name):
            test_event_import.Add_Edit_Test_Event(test_event_id = self.selected_test_event_id,
                                                  test_event_name = name,
                                                  program_id = self.selected_program_id,
                                                  starting_build = starting_build,
                                                  latest_build = latest_build,
                                                  build = build,
                                                  has_multiple_aircraft_types = self.has_multiple_aircraft_types,
                                                  formal = self.formal,
                                                  burndown = self.burndown,
                                                  start_date = self.start_date,
                                                  end_date = self.end_date,
                                                  db_conn = sql_interface.TEST_DATA_DB_CONN,
                                                  gui_handle = self,
                                                  svn_log_file_url = svn_log_file_url)
            
            self.external_link = "https://%(server)s/STARWARS/test_event_status.php?test_family_id=%(family_id)s&test_event_id=%(test_event_id)s"%{
                  'server': sql_interface.TEST_DATA_DB_CONN.server,
                  'family_id':sql_interface.TEST_DATA_DB_CONN.family_id,
                  'test_event_id': self.selected_test_event_id,
            }
            self.linkbutton.set_label(self.external_link)
            
            index = self.test_event_combo.get_active()          
            #re-populate test event list with new test event data
            self.populate_test_event_list()
            self.populate_copy_test_event_list(index)
            #make sure previously selected event is still active after re-populating test event list
            self.test_event_combo.set_active(index)
         # end if is unique or wasn't but we continued anyway
      # end def
     
      def quit(self, widget = None):
         self._print("quitting...")
         sys.exit(0)
      # end def
      
      def switch_family(self, widget):
         #callback to change database or "family"
         if self.debug:
            self._print("switch_family")
         #end if
         sql_interface.TEST_DATA_DB_CONN = sql_interface.Connect_To_Subsystem_Test_Data_Db(prompt_for_subsystem = True)
         self.populate_program_list()
         
         widget = self.connection
         label_string = "Connected to: %(database)s as %(user)s"%{
            'database':sql_interface.TEST_DATA_DB_CONN.database,
            'user':sql_interface.TEST_DATA_DB_CONN.user         }
         self.change_label(widget,label_string)
      # end def
               
      def connect(self):
         self.populate_program_list()
         self.initialized = True
      # end def
      
      def initialize(self):
         #determines if gui has yet been initialized and will print that it is still connecting if not initialized yet
         if self.debug:
            self._print("initialize")
         #end if
         if not self.initialized:
            if self.notify_counter>0:
               self.connect()
            else:
               self._print("Connecting to SQL database...")
            # end if
         else:
            pass
         # end if
         self.notify_counter += 1
         return False
      # end def
      
      def main(self):
         #first function called upon startup
         if self.debug:
            self._print("main")
         #end if
         self.populate_program_list()
         
         #display current user and current database connection
         widget = self.connection
         label_string = "Connected to: %(database)s as %(user)s"%{
            'database':sql_interface.TEST_DATA_DB_CONN.database,
            'user':sql_interface.TEST_DATA_DB_CONN.user         }
         self.change_label(widget,label_string)
         
         
         # All PyGTK applications must have a gtk.main(). Control ends here
         # and waits for an event to occur (like a key press or mouse event).
         gtk.main()
      # end def
      
      def on_Calendar_Select_clicked(self, widget):
         #Opens calendar select popup and determines whether the start or end date is being set
         if self.debug:
            self._print("calendar_select_clicked")
         #end if
         
         #initialization of logic to determine which date filed is to be populated since there is only one function for both signals
         self.start = False
         self.end = False
         which_to_set = None
         #determine and initialize values for start or end date field entry
         if widget == self.calendar_select: 
            self.start = True
            which_to_set = self.start_date
         elif widget == self.calendar_select2: 
            self.end = True
            which_to_set = self.end_date
         #end if
         #determine sizing of calendar which for positioning
         rect = widget.get_allocation()
         x, y = widget.window.get_origin()
         cal_width, cal_height = self.calendar_window.get_size()

         self.calendar_window.show()
         #move calendar window into position just below calendar select field and button
         self.calendar_window.move((x + rect.x - cal_width + rect.width)
                                   , (y + rect.y + rect.height))
         if which_to_set is None:
            #Get current month,day,year subtracting one from month because gtk starts at 0 for this selection
            month_set = int(time.strftime('%m',time.localtime()))-1
            day_set = int(time.strftime('%d',time.localtime()))
            year_set = int(time.strftime('%Y',time.localtime()))
         else:
            month_set = int(time.strftime('%m',time.strptime(which_to_set,self.sql_date_format)))-1
            day_set = int(time.strftime('%d',time.strptime(which_to_set,self.sql_date_format)))
            year_set = int(time.strftime('%Y',time.strptime(which_to_set,self.sql_date_format)))
         #end if
                 
         #set the current date to the calendar popup
         self.cal_widget.select_month(month_set,year_set)
         self.cal_widget.select_day(day_set)   
      #end def
                  
      def change_label(self, widget, label_string):
         widget.set_text(label_string)
      #end def

      def on_calendar_cancel_clicked(self, widget = None):
         #Called when the cancel button on the widget is clicked, thus exiting the window
         
         #Hide the calendar window
         self.calendar_window.hide()
         #re-intialize values for determining start or end date field
         self.start = False
         self.end = False
      #end def
      
      def calendar_widget_day_selected_double_click(self, widget):
         #Called when the user has double-clicked on a date in the calendar widget
         if self.debug:
            self._print("calendar_widget_day_selected_double_click")
         #end if
         
         #Hide the calendar window
         self.calendar_window.hide()

         year, month, day = widget.get_date()
         month +=1 #since it's 0 based
         date_string = "%02d-%02d-%d" % ( month, day, year)
         
         #determine which widget to set text 
         if self.start == True :
            widget = self.start_date_entry
         elif self.end == True :
            widget = self.end_date_entry
         #end if
         widget.set_text(date_string)

         self.date_format(widget)
         #widget argument is optional but determines which date entry to set.
         
         #reintialize values for determining start or end date field
         self.start = False
         self.end = False
      #end def
      
      def linkbutton_callback(self, widget = None):
         #Open webpage with GUI
         webbrowser.open(url = self.external_link,autoraise = 1) 
      #end def
      
      def date_format(self,widget,third = None):
         #format date because display format for the GUI and Database format are different
         if widget == self.start_date_entry:
            try:
               self.start_date = time.strftime(self.sql_date_format,time.strptime(self.start_date_entry.get_text(),self.display_format))
               self._print("Start Date: %s"%str(self.start_date))
            except ValueError:
               widget.set_text("mm-dd-yyyy")
         elif widget == self.end_date_entry:
            try: 
               self.end_date = time.strftime(self.sql_date_format,time.strptime(self.end_date_entry.get_text(),self.display_format))
               self._print("End Date: %s"%str(self.end_date))
            except ValueError:
               widget.set_text("mm-dd-yyyy")
         else:
            self._print("Unexpected widget")
         #end if
      #end def
      
      def on_cancel(self,widget = None):
         self.cancelled = True
         self._print("Cancelled")
         self.progress_window.hide()
      #end def
      
      def show_progress(self,update_what= None):
         #show popup and center on GUI
         x, y = self.window.window.get_origin()
         window_width, window_height = self.window.get_size()
         prog_width, prog_height = self.progress_window.get_size()
         self.cancelled = False
         self.progress_window.show()
         self.progress_window.move((x + window_width/2 - prog_width/2), (y + window_height/2 - prog_height))
         self.progress_window.set_title("Update Progress (%s)"%update_what)
      #end def
      
      def populate_assets_available_list(self):
         #determine list of assets available for use and display in available assets treeview
         if self.debug:
            self._print("populate_assets_available_list")
         #end if
         self.available_assets_tree_store.clear()
         self.available_assets_dict = test_event_import.populate_available_assets(self.selected_test_event_id,db_conn = sql_interface.TEST_DATA_DB_CONN)
         #build list for treeview
         for row in self.available_assets_dict:
            row_list = ["%s (%s)"%(row['test_asset_nickname'],row['test_asset_machine_name'])]
            self.available_assets_tree_store.append(None,row_list)
         #end for
         self.available_assets.set_model(self.available_assets_tree_store)
         
      #end def
      
      def populate_assets_in_event(self):
         #determine list of assets already associated to the test event and display them in assets_in_event treeview
         if self.debug:
            self._print("populate_assets_in_event")
         #end if
         self.test_event_assets_tree_store.clear()
         self.asset_in_column.set_title("Assets for %s"%self.selected_test_event_name)
         self.test_event_assets_dict = test_event_import.populate_event_assets(self.selected_test_event_id,db_conn = sql_interface.TEST_DATA_DB_CONN)
         #build list for treeview
         for row in self.test_event_assets_dict:
            row_list = ["%s (%s)"%(row['test_asset_nickname'],row['test_asset_machine_name'])]
            self.test_event_assets_tree_store.append(None,row_list)
         #end for
         self.test_event_assets.set_model(self.test_event_assets_tree_store)
      #end def
       
      def add_asset(self, widget = None):
         #associate asset from available assets list to selected test event
         if self.debug:
            self._print("add_asset")
         #end if
         data = sql_interface.Call("add_test_asset_to_event",(self.selected_test_event_id,self.selected_test_asset_id),db_conn = sql_interface.TEST_DATA_DB_CONN)
         for select in data:     # loop through the various 'select' outputs from the stored proc
            for row in select:   # loop through the rows in each select statement from the stored proc
               if 'success' in row.keys(): # if we found the row in the select that we are looking for
                  success = row['success']
                  message = row['message']
                  # at this point, since we found what we wanted, and we don't need anything else, bail
                  done = True;
                  break;
               # end if
            # end for each dictionary
            if done: break
         # end for each tuple
         if success == 0:
            self._print(message)
         #end if
         if len(str(sql_interface.sql_warning_message)) > 0:
            self._warning("\n%s\n"%str(sql_interface.sql_warning_message))
         #end if
         
         self.populate_assets_available_list()
         self.populate_assets_in_event()
      #end def
      
      def remove_asset(self,widget = None,asset = None):
         #remove associated test asset from selected test event
         if self.debug:
            self._print("remove_asset")
         #end if
         if asset is None:
            asset = self.selected_test_asset_id
         #end if
         data = sql_interface.Call("remove_test_asset_from_event",(self.selected_test_event_id,asset),db_conn = sql_interface.TEST_DATA_DB_CONN)
         for select in data:     # loop through the various 'select' outputs from the stored proc
            for row in select:   # loop through the rows in each select statement from the stored proc
               if 'success' in row.keys(): # if we found the row in the select that we are looking for
                  success = row['success']
                  message = row['message']
                  # at this point, since we found what we wanted, and we don't need anything else, bail
                  done = True;
                  break;
               # end if
            # end for each dictionary
            if done: break
         # end for each tuple         
         if success == 0:
            self._print(message)
         #end if
         if len(str(sql_interface.sql_warning_message)) > 0:
            self._warning("\n%s\n"%str(sql_interface.sql_warning_message))
         #end if
         
         self.populate_assets_available_list()
         self.populate_assets_in_event()
      #end def
      
      def clear_list(self, widget = None):
         #clear all associated test events for selected test event
         for row in self.test_event_assets_dict:
            asset = row['test_asset_id']
            self.remove_asset(asset = asset)
         #end for
      #end def
      
      def change_assets(self, widget = None):
         #edit or create new test asset to be added to list of available test assets
         if self.debug:
            self._print("change_assets")
         #end if
         self.test_asset_nickname = self.asset_nickname_entry.get_text()
         self.test_asset_machine_name = self.asset_machname_entry.get_text()
         self.num_cdus_used = self.num_cdus_entry.get_text()
         if self.cdu_power_entry.get_active() is True:
            self.cdu_power = 1
         else:
            self.cdu_power = 0
         #end if
         #use logic to determine if the asset is to be created or updated
         if self.create is True:
            data = sql_interface.Call("create_test_asset",(self.test_asset_nickname,
                                                 self.test_asset_machine_name,
                                                 self.num_cdus_used,
                                                 self.cdu_power),
                                                 db_conn = sql_interface.TEST_DATA_DB_CONN)
            for select in data:     # loop through the various 'select' outputs from the stored proc
               for row in select:   # loop through the rows in each select statement from the stored proc
                  if 'success' in row.keys(): # if we found the row in the select that we are looking for
                     success = row['success']
                     test_asset_id = row['test_asset_id']
                     message = row['message']
                     # at this point, since we found what we wanted, and we don't need anything else, bail
                     done = True;
                     break;
                  # end if
               # end for each dictionary
               if done: break
            # end for each tuple            
            if success == 1:
               self._print("Asset Created")
            elif success == 0:
               self._print(str(message))
            #end if
         else:
            data = sql_interface.Call("update_test_asset",(self.selected_test_asset_id,
                                                    self.test_asset_nickname,
                                                    self.test_asset_machine_name,
                                                    self.num_cdus_used,
                                                    self.cdu_power),
                                                    db_conn = sql_interface.TEST_DATA_DB_CONN)
            for select in data:     # loop through the various 'select' outputs from the stored proc
               for row in select:   # loop through the rows in each select statement from the stored proc
                  if 'success' in row.keys(): # if we found the row in the select that we are looking for
                     success = row['success']
                     message = row['message']
                     # at this point, since we found what we wanted, and we don't need anything else, bail
                     done = True;
                     break;
                  # end if
               # end for each dictionary
               if done: break
            # end for each tuple
            if success == 1:
               self._print("Asset Updated")
            elif success == 0:
               self._print(str(message))
            #end if
         #end if
         if len(str(sql_interface.sql_warning_message)) > 0:
            self._warning("\n%s\n"%str(sql_interface.sql_warning_message))
         #end if
         
         #hide asset edit/create window and repopulate both lists even test assets to include new information
         self.test_asset_window.hide()
         self.populate_assets_available_list()
         self.populate_assets_in_event()
      #end def
      
      def select_test_asset_in(self, widget = None, widgetreturn = None):
         #determine selected test asset in selected test event and associated information with asset
         object,entry = self.test_event_assets.get_selection().get_selected()
         row = int(object.get_path(entry)[0])
         #unselect other widgets row for clarity
         self.available_assets.get_selection().unselect_all()
         self.test_asset_nickname = self.test_event_assets_dict[row]['test_asset_nickname']
         self.test_asset_machine_name = self.test_event_assets_dict[row]['test_asset_machine_name']
         self.num_cdus_used = self.test_event_assets_dict[row]['num_cdus']
         self.cdu_power = self.test_event_assets_dict[row]['cdu_power']
         if self.cdu_power == 0:
            self.cdu_power_state = False
         else:
            self.cdu_power_state = True
         #end if
         self.selected_test_asset_id = self.test_event_assets_dict[row]['test_asset_id'] #somehow set selected as select row
      #end def      
      
      def select_test_asset(self, widget = None, widgetreturn = None):
         #determine selected available test asset and associated information with asset
         object,entry = self.available_assets.get_selection().get_selected()
         row = int(object.get_path(entry)[0])
         #unselect other widgets row for clarity
         self.test_event_assets.get_selection().unselect_all()
         self.test_asset_nickname = self.available_assets_dict[row]['test_asset_nickname']
         self.test_asset_machine_name = self.available_assets_dict[row]['test_asset_machine_name']
         self.num_cdus_used = self.available_assets_dict[row]['num_cdus']
         self.cdu_power = self.available_assets_dict[row]['cdu_power']
         if self.cdu_power == 0:
            self.cdu_power_state = False
         else:
            self.cdu_power_state = True
         #end if
         self.selected_test_asset_id = self.available_assets_dict[row]['test_asset_id'] #somehow set selected as select row
      #end def
      
      def show_asset_edit(self, widget = None, widgetreturn = None):
         #show asset edit/create popup and center on GUI
         skip = False
         if widget == self.create_asset:
            self.create = True
            #initialize fields
            self.test_asset_nickname = None
            self.test_asset_machine_name = None
            self.num_cdus_used = None
            self.cdu_power = False
            self.asset_nickname_entry.set_text("")
            self.asset_machname_entry.set_text("")
            self.num_cdus_entry.set_text("")
            self.asset_id_label.set_text("None")
            self.cdu_power_entry.set_active(self.cdu_power)

            do_what_with_assets = "Create Asset"
            asset_button_text = "Create"
         else:
            try:
               self.create = False
               self.asset_nickname_entry.set_text(self.test_asset_nickname)
               self.asset_machname_entry.set_text(self.test_asset_machine_name)
               self.num_cdus_entry.set_text(str(self.num_cdus_used))
               self.cdu_power_entry.set_active(self.cdu_power)
               self.asset_id_label.set_text(str(self.selected_test_asset_id))
               do_what_with_assets = "Edit Asset"
               asset_button_text = "Update"
            except:
               self._print("Select a test asset to edit")
               skip = True
         #end if
         if not skip:
            x, y = self.window.window.get_origin()
            window_width, window_height = self.window.get_size()
            asset_window_width, asset_window_height = self.test_asset_window.get_size()
            self.test_asset_window.show()
            self.test_asset_window.move((x + window_width/2 - asset_window_width/2), (y + window_height/2 - asset_window_height))
            self.test_asset_window.set_title("%s"%do_what_with_assets)
            self.test_asset_button.set_label("%s"%asset_button_text)
         #end if
      
      def asset_edit_cancel(self, widget = None):
         self.test_asset_window.hide()
      #end def
      
      def to_asset_management(self, widget = None):
         self.page_notebook.set_current_page(self.asset_page_num)
      #end def
      
      def default_to_page(self,widget = None):
         self.page_notebook.set_current_page(self.default_to_page_num)
      #end def
      
      def _warning(self, text):
         x, y = self.window.window.get_origin()
         window_width, window_height = self.window.get_size()
         warning_window_width, warning_window_height = self.warning_window.get_size()
         self.warning_window.show()
         self.warning_window.move((x + window_width/2 - warning_window_width/2), (y + window_height/2 - warning_window_height))
         self.warning_window.set_title("WARNING!")
         self.warning_message.set_text(text)
      #end def
      
      def warning_ok(self, widget = None):
         self.warning_window.hide()
      #end def
      
      def connect_tldb(self, widget = None):
         try:
            import tldb_sql_interface
            import copy_results_to_tldb
            self.tldb_sql_interface = tldb_sql_interface
            self.copy_results_to_tldb = copy_results_to_tldb
            self.populate_tldb_programs()
            self.connected = True
         except:
            pass
      #end def
      
      def tldb_program_callback(self, widget):
         index = self.tldb_program_combo.get_active()
         if index is not 0:
            self.selected_tldb_program = self.tldb_programs[index-1]['program']
            self.populate_tldb_events()
         else:
            self.tldb_event_combo.set_active(0)
         #end if
      #end def
      
      def tldb_test_event_callback(self, widget):
         index = self.tldb_event_combo.get_active()
         if index is not 0:
            self.selected_tldb_event = self.tldb_events[index-1]['Test Event ID']
            self.populate_tldb_descriptions()
         else:
            self.tldb_description_combo.set_active(0)
         #end if
      
      #end def
      
      def tldb_description_callback(self, widget):
         index = self.tldb_description_combo.get_active()
         if index is not 0:
            self.selected_tldb_description_id = self.tldb_descriptions[index-1]['Test Description ID']
         #end if
      #end def
      
      def populate_tldb_programs(self):
         self.tldb_programs = self.tldb_sql_interface.Get_All_Programs()
         program_list = gtk.ListStore(str)
         program_list.append(["Select a program..."])
         for i in range(0,len(self.tldb_programs)):
            program_list.append(["%s"%(self.tldb_programs[i]["program"])])
         #end for
         self.tldb_program_combo.set_model(program_list)
         self.tldb_program_combo.set_active(0)
      #end def
      
      def populate_tldb_events(self):
         self.tldb_events = self.tldb_sql_interface.Get_All_Test_Events_For_This_Program(self.selected_tldb_program)
         events_list = gtk.ListStore(str)
         events_list.append(["Select a Test Event.."])
         for i in range(0,len(self.tldb_events)):
            events_list.append(["%s"%(self.tldb_events[i]["Test Event"])])
         #end for
         self.tldb_event_combo.set_model(events_list)
         self.tldb_event_combo.set_active(0)
      #end def
      
      def populate_tldb_descriptions(self):
         self.tldb_descriptions = self.tldb_sql_interface.Get_All_Descriptions(self.selected_tldb_event)
         description_list = gtk.ListStore(str)
         description_list.append(["Select a Description"])
         for i in range(0,len(self.tldb_descriptions)):
            description_list.append(["%s"%(self.tldb_descriptions[i]["Description"])])
         #end for
         self.tldb_description_combo.set_model(description_list)
         self.tldb_description_combo.set_active(0)
      #end def
      
      def sync(self,widget = None):
         if self.connected:
            if self.selected_tldb_description_id and self.selected_test_event_id:
               self.show_progress("Sync TLDB Test Runs/Issues")  
               if self.debug:
                  copy_results_to_tldb = self.copy_results_to_tldb
                  reload(copy_results_to_tldb)
                  self.copy_results_to_tldb = copy_results_to_tldb
               # end if
               self.copy_results_to_tldb.Copy_Test_Runs_And_Issues_To_TLDB(test_event_id = self.selected_test_event_id, tldb_description_id = self.selected_tldb_description_id, gui_handle = self, debug = self.debug)
               print '1'
               self.progress_window.hide()
               print '2'
            else:
               self._warning("You need to select a TLDB Program, TLDB Test Event, and TLDB Description\nin addition to selecting a Program and Test Event to copy to the TLDB.")
            #end if
         else:
            self._warning("You need to connect to the TLDB")
         #end if
         print 'done sync'
      #end def
      def create_section_list(self,widget = None):
         import create_tldb_section_list
         # creating a section list only depends on the local DB
         # connection -- it does not sync or connect to the TLDB
         # not dependent upon connection to TLDB
         if self.selected_program_id:
            if self.selected_test_event_id:
               self.show_progress("Export Section List to CSV")
               create_tldb_section_list.do_export(
                                    program_id = self.selected_program_id,
                                    test_event_id =self.selected_test_event_id, 
                                    gui_handle = self, debug = self.debug)
               self.progress_window.hide()
            else:
               self._warning("You must select a test event from the current program to create a section list")
            #end if
         else:
            self._warning("You must select a program from the current family\nto create a section list")
         #end if
      # end def
      def export_section_list_to_tldb(self, widget=None):
         import create_tldb_section_list
         if self.connected:
            if self.selected_tldb_description_id and self.selected_test_event_id:
               self.show_progress("Sync TLDB Section List")
               create_tldb_section_list.do_export_to_tldb(
                        program_id = self.selected_program_id,
                        test_event_id =self.selected_test_event_id,
                        tldb_description_id = self.selected_tldb_description_id, 
                        gui_handle = self, debug = self.debug)
               self.progress_window.hide()
            else:
               self._warning("You need to select a TLDB Program, TLDB Test Event, and TLDB Description\nin addition to selecting a Program and Test Event to copy to the TLDB.")
            #end if
         else:
            self._warning("You need to connect to the TLDB")
         #end if
         self._warning("done export_section_list_to_tldb")
      # end def export_section_list_to_tldb
   #end class
      
   if __name__ == "__main__":
      teGUI = UpdateTestEventGUI()
      teGUI.main()
   # end if
except:
   import traceback
   traceback.print_exc(file=sys.stdout)
   import pdb; pdb.set_trace()
# end try
