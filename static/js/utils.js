/*------------------------------Navbar, transparente => sólido------------------------------*/
jQuery(function () {
    jQuery(window).scroll(function () {
        if (jQuery(this).scrollTop() > 50) {
            $("#navbar-default").css('background-color', 'rgb(27, 38, 49)');
        } else {
            $("#navbar-default").css('background-color', 'rgba(27, 38, 49, 0.7)');
        }
    });
});