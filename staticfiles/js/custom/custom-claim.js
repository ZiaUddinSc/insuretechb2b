$(document).ready(function(){
    $('#beneficiary-search').keyup(function(){
      
        var query = $(this).val();
        alert(query)
        if (query.length > 1){
            $.ajax({
                url: '/claim/suggest/',
                data: {
                    'term': query
                },
                dataType: 'json',
                success: function(data){
                    let suggestions = '';
                    data.forEach(function(item){
                        suggestions += '<div class="suggest-item">' + item + '</div>';
                    });
                    $('#suggestions').html(suggestions).show();
                }
            });
        } else {
            $('#suggestions').hide();
        }
    });

    // Optionally handle item click
    $(document).on('click', '.suggest-item', function(){
        $('#pbeneficiary-search').val($(this).text());
        $('#suggestions').hide();
    });
});