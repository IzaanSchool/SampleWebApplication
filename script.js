$('form').on('submit', function () {
    event.preventDefault();
    $(this).find('.form-control').each(function () {
      var id = $(this).attr('id').replace('field', '');
      $('.results' + id).text($(this).val());
    });
  });