/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false */
'use strict';

(function ($) {

    $(document).pjax('a[data-pjax]', '#app-pjax-container', { fragment: '#content-core' });

    $(document).ready(function () {
        if ($('body').hasClass('lt-ie7')) {return; }
        // if ($.support.pjax) {
        //     $(document).on('click', 'a[data-pjax]', function (event) {
        //         var container = $(this).closest('[data-pjax-container]');
        //         $.pjax.click(event, {container: container});
        //     });
        // }
        $('div[data-appui="editable"]').on({
            mouseenter: function () {
                $(this).find('.contentpanel-editbar').removeClass('fadeOutUp').addClass('fadeInLeft').show();
            },
            mouseleave: function () {
                $(this).find('.contentpanel-editbar').removeClass('fadeInLeft').addClass('fadeOutUp');
            }
        });
        $('a[data-appui="overslide"]').on({
            click: function (e) {
                e.preventDefault();
                var targetBlock = $(this).data('target');
                // $(this).parent().removeClass('bounceInLeft').addClass('bounceOutRight');
                if ($(targetBlock).hasClass('fadeOutTop')) {
                    $(targetBlock).removeClass('fadeOutTop').addClass('slideInRight').show();
                } else {
                    $(targetBlock).addClass('slideInRight').show();
                }
            }
        });
        $('a[data-appui="overslide-close"]').on({
            click: function (e) {
                e.preventDefault();
                $(this).closest('.panelpage-slide').removeClass('slideInRight').addClass('fadeOutTop').hide();
            }
        });
    }
    );
}(jQuery));
