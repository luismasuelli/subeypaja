(function($){
    $.fn.serializeObject = $.fn.serializeObject || function()  {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

    $(function(){
        $(document).on('submit', 'form.asynchronous', function() {
            var form = this;
            var $form = $(form);

            var method = ($form.attr('method') || 'get').toLowerCase();
            var action = ($form.attr('action') || '');
            var enctype = ($form.attr('enctype') || '').toLowerCase().trim();

            // enctype may be: multipart/form-data, application/x-www-form-urlencoded, text/plain, application/json
            var data;
            switch(enctype) {
                case 'application/json':
                    data = JSON.stringify($form.serializeObject());
                    break;
                case 'multipart/form-data':
                    data = new FormData(form);
                    break;
                //case 'application/x-www-form-urlencoded':
                //case 'text/plain':
                default:
                    data = $form.serialize();
            }

            if (['application/json', 'multipart/form-data', 'text/plain',
                 'application/x-www-form-urlencoded'].indexOf(enctype) < 0) {
                enctype = 'application/x-www-form-urlencoded';
            }

            // extra data may be added if attribute data-fetcher="foo" exists,
            //   and window.foo() can be called
            var fetcher = $form.data('fetcher');
            var baseObj = {};
            if (fetcher) {
                fetcher = window[fetcher];
                if (typeof fetcher === 'function') {
                    baseObj = fetcher($form);
                }
            }

            var settings = $.extend({}, baseObj, {
                contentType: enctype,
                url: action,
                method: method,
                data: data,
                success: function(data, statusText, xhr) { $form.trigger('async:success', [data, statusText, xhr]); },
                error: function(xhr, statusText, errorText) { $form.trigger('async:error', [xhr, statusText, errorText]) },
                complete: function(xhr, statusText) { $form.trigger('async:complete', [xhr, statusText]); }
            });

            $.ajax(settings);
            return false;
        })
    });
})(jQuery);