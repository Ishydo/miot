import $ from 'jquery'

import 'tether/dist/js/tether.min.js'
import 'tether/dist/css/tether.min.css'

import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import './style.css'

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
