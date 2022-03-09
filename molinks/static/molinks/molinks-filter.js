// Mo Links table filter
// Copyright (c) 2022 Stephen Krauth
// All rights reserved

// Filters a table based on search term typed into a text input box; rows with no matches in
// any searched TD element will be hidden, and matching rows will have the first occurance of
// the search term highlighted with a MARK tag

// How to use:
// - Create a text input box with an id
// - Create a table with an id and assign ids to the various TD elements you want to search
// - Initialize molinks.filter:
// 
//  <script>
//      molinks.filter({
//          input_id: "filterbox",
//          table_id: "filtertable",
//          td_plain_classes: ['classB', 'classC'],
//          td_link_classes:  ['classA'],
//      });
//  </script>
//
// Search term will be searched for in TD elements matching the "td_plain_classes", and in
// links within TD elements matching the "td_link_classes".
//
// See below for full list of available options.

// global namespace object
var molinks = molinks || {};

// module
molinks.filter = (function() {
    // default settings
    var defaults = {
        // td classes to search (at least one required)
        td_plain_classes:   [],     // directly search TD contents
        td_link_classes:    [],     // search link text within TD

        // configuration (ie. optional)
        input_id:           "filterbox",
        table_id:           "filtertable",
        dirty_flag:         "filter-dirty-flag",
        typing_delay:       125,
    }

    // globals
    var timeout;

    function init(options) {
        // setup options
        var settings = {};
        for (var prop in defaults) {
            settings[prop] = defaults[prop];
        }
        for (var prop in options) {
            settings[prop] = options[prop];
        }

        // check required args
        if (settings.td_plain_classes.length + settings.td_link_classes.length == 0) {
            console.log(`molinks.filter error: no td classes have been specified to search`);
            return;
        }

        // setup callback
        filterbox = document.getElementById(settings.input_id);
        if (filterbox == null) {
            console.log(`molinks.filter error: no element found with id "${settings.input_id}"`);
            return;
        }
        filter_event = function(event) {
            filter(event, filterbox, settings);
        }
        filterbox.onkeyup = filter_event;
    }

    // main filter entry point
    function filter(event, filterbox, settings) {
        if (timeout) {
            clearTimeout(timeout);
        }

        // ignore bad events
        if (! event.target) {
            return null;
        }

        // bind ESC key to immediately clear filter box
        if (event && ('keyCode' in event) && (event.keyCode == 27)) {
            filterbox.value = "";
            doFilter(filterbox, settings);
        }

        // do nothing if only a single character is in the filterbox
        if (filterbox.value.length == 1) {
            return;
        }

        // do filtering after a timeout to handle typing delay
        timeout = setTimeout(function() {
            doFilter(filterbox, settings);
        }, settings.typing_delay);
    }

    // do the filtering
    function doFilter(filterbox, settings) {
        var find = filterbox.value.toLowerCase();
        var table = document.getElementById(settings.table_id);

        // remember previous search string to prevent unnecessary searches
        if (typeof filterbox.previous != 'undefined') {
            if (find == filterbox.previous) {
                return;
            }
        }
        filterbox.previous = find;

        // do nothing if filterbox is clear and table is clean
        if (find.length == 0 && ! table.classList.contains(settings.dirty_flag)) {
            return;
        }

        var trs = table.getElementsByTagName("tr");

        // restore table if filterbox is clear (because table is dirty if we made it here)
        if (find.length == 0) {
            for (var tr of trs) {
                tr.style.visibility = "";
                clean(tr);
            }
            table.classList.remove(settings.dirty_flag);
            return;
        }

        // do the thing
        var groupShown = 0;
        var hidden = 0;
        var header = null;
        for (var tr of trs) {
            var tds = tr.getElementsByTagName("td");
            var ths = tr.getElementsByTagName("th");
            var show = false;

            // header row
            if (ths.length > 0) {
                handleHeader(header, groupShown);
                header = tr;
                groupShown = 0;

            // link row
            } else {
                var index, elem;
                for (var td of tds) {
                    if (settings.td_plain_classes.some((c) => { return td.classList.contains(c); })) {
                        index = td.textContent.toLowerCase().indexOf(find);
                        if (index > -1) {
                            show = true;
                            elem = td;
                            break;
                        }
                    } else if (settings.td_link_classes.some((c) => { return td.classList.contains(c); })) {
                        index = td.children[0].textContent.toLowerCase().indexOf(find);
                        if (index > -1) {
                            show = true;
                            elem = td.children[0];
                            break;
                        }
                    }
                }
                if (show) {
                    markAndShow(tr, elem, filterbox.value.length, index);
                    groupShown++;
                } else {
                    cleanAndHide(tr, elem);
                    hidden++;
                }
            }
        }
        // last header
        handleHeader(header, groupShown);

        // mark table dirty or clean
        if (hidden > 0) {
            table.classList.add(settings.dirty_flag);
        } else {
            table.classList.remove(settings.dirty_flag);
        }
    }

    // ---- filter helpers --------------------------------------------------------------------------------

    function handleHeader(header, groupShown) {
        if (header) {
            if (groupShown > 0) {
                header.style.visibility = "";
            } else {
                header.style.visibility = "collapse";
            }
        }
    }

    function clean(tr) {
        for (var mark of tr.getElementsByTagName('mark')) {
            // undo and whitespace overrides we added to show marks
            mark.parentElement.style.whiteSpace = "";
            mark.parentElement.innerHTML = mark.parentElement.textContent;
        }
    }

    function markAndShow(tr, elem, len, index) {
        tr.style.visibility = "";
        clean(tr);
        var t = elem.textContent;
        elem.innerHTML = t.substr(0, index) + "<mark>" + t.substr(index, len) + "</mark>" + t.substr(index + len)
        // disable nowrap on links to show marks that might be hidden by overflow
        if (elem.parentElement.classList.contains('linkcolumn')) {
            elem.style.whiteSpace = "normal";
        }
    }

    function cleanAndHide(tr) {
        tr.style.visibility = "collapse";
        clean(tr);
    }

    // expose init function as the public interface
    return init;
}());
