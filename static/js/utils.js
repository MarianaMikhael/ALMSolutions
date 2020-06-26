/*------------------------------Navbar, transparente => sólido------------------------------*/
jQuery(function () {
    jQuery(window).scroll(function () {
        if (jQuery(this).scrollTop() > 50) {
            $("#navbar-default").css('background-color', 'rgb(0, 51, 255, 0.075)');
        } else {
            $("#navbar-default").css('background-color', 'rgba(0, 51, 255, 0)');
        }
    });
});