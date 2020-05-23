
$(document).ready(function() {

    const $toggleButton = $('.toggle-button'),
        $menuWrap = $('.menu-wrap'),
        $sidebarArrow = $('.sidebar-menu-arrow');

    $toggleButton.on('click', function() {
        $(this).toggleClass('button-open');
        $menuWrap.toggleClass('menu-show');
    });

    $sidebarArrow.click(function() {
        $(this).next().slideToggle(300);
    });

});