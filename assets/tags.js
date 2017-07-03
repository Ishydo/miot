console.log("Hello world")

$(() => {
  $('.tags-input').tagsInput({
    'defaultText':'Add a tag',
    'delimiter': [',',';'],
    'width': '100%',
  })
})
