/**
 * Created by gvammer on 16.11.15.
 */
function initSpecialtiesFind(addFunc, deleteFunc) {
   var $specialtyInput = $('.js-save_specialty'),
    $searchDropdown = $('.js-search_specialties'),
    $specialties = $('.js-specialties');

    var appendSkills = function (id, name) {
        var $specialty = ('<li><input type="hidden" name="tag[]" value="' + name + '" /><span class="tag-name">' + name + '</span><span class="tag-num"><i class="fa fa-times tag-num-icon js-delete_specialty"' +
        'data-specialty="' + id + '"></i></span></span></li>');
        $specialties.append($specialty);
        if ($specialties.hasClass('hidden')) {
            $specialties.removeClass('hidden')
        }
    };

    $specialtyInput.keypress(function(e) {
        var $t = $(this);
        var key = e.keyCode;
        if (key == 13) { // Enter key
            addFunc($t, appendSkills, $searchDropdown);
        }
        if (key == 40) { // Down key
            $searchDropdown.find('li:visible').removeClass('active').eq(0).addClass('active').find('a').focus()
        }
    }).on('click', function(e) {e.stopPropagation();});

    $searchDropdown.keypress(function (e) {
        var key = e.keyCode;

        if (key == 40) { //down
            if ($(this).find('li.active').is(':last-child')) {
                return false
            } else {
                $(this).find('li.active').removeClass('active').next(':visible').addClass('active').find('a').focus();
            }
            return false;
        } else if (key == 38) { //up
            if ($(this).find('li.active').is(':first-child')) {
                $(this).find('li.active').removeClass('active');
                $specialtyInput.focus()
            } else {
                $(this).find('li.active').removeClass('active').prev(':visible').addClass('active').find('a').focus();
            }
            return false;
        } else if (key == 13) {
            $specialtyInput.val($(this).find('a').text()).focus();
            $searchDropdown.hide();
        }
    });

    $searchDropdown.on('click', '*', function(e) {
        e.stopPropagation();
        $specialtyInput.val($(this).text()).focus();
        $searchDropdown.hide();
    });

    $searchDropdown.on('mouseover', 'li', (function() {
        $(this).activateListItem().find('a').blur()
    }));

    $(document).on('click', '.js-delete_specialty', function () {
        var $t = $(this);
        deleteFunc($t);
    });

    var search_val = null;
    $specialtyInput.keyup(function() {
        var $t = $(this);
        if ($t.val() != search_val) {
            search_val = $t.val();
            if (search_val.length > 2) {
                $.post(
                    '/ajax/specialty/',
                    {
                        'action': 'specialty_search',
                        'search_text': $t.val(),
                        'user': $t.data('user-id')
                    },
                    function (response) {
                        var data = $.parseJSON(response);
                        if (data.length > 0) {
                            $searchDropdown.empty();
                            for (var i = 0; i < data.length; i++) {
                                var $skill = $('<li><a href=#>' + data[i] + '</a></li>');
                                $searchDropdown.append($skill)
                            }
                            $searchDropdown.show()
                        }
                    }
                )
            }
        }
    });

    $(document).on('click', function() {
        $searchDropdown.hide()
    });
}