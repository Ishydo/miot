console.log("Loading dashboard JS.")

import 'jquery-tags-input/dist/jquery.tagsinput.min.css'
import 'jquery-tags-input/dist/jquery.tagsinput.min.js'
import './tags.js'

// Core - these two are required :-)
import tinymce from 'tinymce/tinymce.min.js'
import 'tinymce/themes/modern/theme.min.js'
import 'tinymce/skins/lightgray/skin.min.css'

tinymce.init({
  selector: ".tinymce-editor",
  skin: false,
  setup: function (editor) {
    editor.on('change', function () {
      editor.save();
    });
  }
});

import 'sortablejs'


// The CSS
import './dashboard.css'
