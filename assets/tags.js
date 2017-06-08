console.log("Hello world")

$(() => {
  $('.tags-input').tagsInput({
    'defaultText':'add a tag',
    'delimiter': [',', ', ', ';'],
    'width': '100%',
  })
})
