// jquery
import $ from 'jquery'

// Tether needed for some bootstrap components
import 'tether/dist/js/tether.min.js'
import 'tether/dist/css/tether.min.css'

// The bootstrap
import 'bootstrap/dist/js/bootstrap.min.js'
import 'bootstrap/dist/css/bootstrap.min.css'
import './style.css'

// Tooltip initialisation
$(() => {
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })
})
