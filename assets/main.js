import $ from 'jquery'

import 'tether/dist/js/tether.min.js'
import 'tether/dist/css/tether.min.css'

import 'bootstrap/dist/js/bootstrap.min.js'
import 'bootstrap/dist/css/bootstrap.min.css'
import './style.css'

$(() => {
  $(function () {
    console.log("tooltip");
    $('[data-toggle="tooltip"]').tooltip()
  })
})
