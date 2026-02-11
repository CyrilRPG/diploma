/*
	Editorial by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$head = $('head'),
		$body = $('body');

	// Breakpoints.
		breakpoints({
			xlarge:   [ '1281px',  '1680px' ],
			large:    [ '981px',   '1280px' ],
			medium:   [ '737px',   '980px'  ],
			small:    [ '481px',   '736px'  ],
			xsmall:   [ '361px',   '480px'  ],
			xxsmall:  [ null,      '360px'  ],
			'xlarge-to-max':    '(min-width: 1681px)',
			'small-to-xlarge':  '(min-width: 481px) and (max-width: 1680px)'
		});

	// Stops animations/transitions until the page has ...

		// ... loaded.
			$window.on('load', function() {
				window.setTimeout(function() {
					$body.removeClass('is-preload');
				}, 100);
			});

		// ... stopped resizing.
			var resizeTimeout;

			$window.on('resize', function() {

				// Mark as resizing.
					$body.addClass('is-resizing');

				// Unmark after delay.
					clearTimeout(resizeTimeout);

					resizeTimeout = setTimeout(function() {
						$body.removeClass('is-resizing');
					}, 100);

			});

	// Fixes.

		// Object fit images.
			if (!browser.canUse('object-fit')
			||	browser.name == 'safari')
				$('.image.object').each(function() {

					var $this = $(this),
						$img = $this.children('img');

					// Hide original image.
						$img.css('opacity', '0');

					// Set background.
						$this
							.css('background-image', 'url("' + $img.attr('src') + '")')
							.css('background-size', $img.css('object-fit') ? $img.css('object-fit') : 'cover')
							.css('background-position', $img.css('object-position') ? $img.css('object-position') : 'center');

				});

	// Sidebar.
		var $sidebar = $('#sidebar'),
			$sidebar_inner = $sidebar.children('.inner');

		// Inactive by default on <= large.
			breakpoints.on('<=large', function() {
				$sidebar.addClass('inactive');
			});

			breakpoints.on('>large', function() {
				$sidebar.removeClass('inactive');
			});

		// Hack: Workaround for Chrome/Android scrollbar position bug.
			if (browser.os == 'android'
			&&	browser.name == 'chrome')
				$('<style>#sidebar .inner::-webkit-scrollbar { display: none; }</style>')
					.appendTo($head);

		// Toggle.
			$('<a href="#sidebar" class="toggle">Toggle</a>')
				.appendTo($sidebar)
				.on('click', function(event) {

					// Prevent default.
						event.preventDefault();
						event.stopPropagation();

					// Toggle.
						$sidebar.toggleClass('inactive');

				});

		// Events.

			// Link clicks.
				$sidebar.on('click', 'a', function(event) {

					// >large? Bail.
						if (breakpoints.active('>large'))
							return;

					// Vars.
						var $a = $(this),
							href = $a.attr('href'),
							target = $a.attr('target');

					// Prevent default.
						event.preventDefault();
						event.stopPropagation();

					// Check URL.
						if (!href || href == '#' || href == '')
							return;

					// Hide sidebar.
						$sidebar.addClass('inactive');

					// Redirect to href.
						setTimeout(function() {

							if (target == '_blank')
								window.open(href);
							else
								window.location.href = href;

						}, 500);

				});

			// Prevent certain events inside the panel from bubbling.
				$sidebar.on('click touchend touchstart touchmove', function(event) {

					// >large? Bail.
						if (breakpoints.active('>large'))
							return;

					// Prevent propagation.
						event.stopPropagation();

				});

			// Hide panel on body click/tap.
				$body.on('click touchend', function(event) {

					// >large? Bail.
						if (breakpoints.active('>large'))
							return;

					// Deactivate.
						$sidebar.addClass('inactive');

				});

		// Scroll lock.
		// Note: If you do anything to change the height of the sidebar's content, be sure to
		// trigger 'resize.sidebar-lock' on $window so stuff doesn't get out of sync.

			$window.on('load.sidebar-lock', function() {

				var sh, wh, st;

				// Reset scroll position to 0 if it's 1.
					if ($window.scrollTop() == 1)
						$window.scrollTop(0);

				$window
					.on('scroll.sidebar-lock', function() {

						var x, y;

						// <=large? Bail.
							if (breakpoints.active('<=large')) {

								$sidebar_inner
									.data('locked', 0)
									.css('position', '')
									.css('top', '');

								return;

							}

						// Calculate positions.
							x = Math.max(sh - wh, 0);
							y = Math.max(0, $window.scrollTop() - x);

						// Lock/unlock.
							if ($sidebar_inner.data('locked') == 1) {

								if (y <= 0)
									$sidebar_inner
										.data('locked', 0)
										.css('position', '')
										.css('top', '');
								else
									$sidebar_inner
										.css('top', -1 * x);

							}
							else {

								if (y > 0)
									$sidebar_inner
										.data('locked', 1)
										.css('position', 'fixed')
										.css('top', -1 * x);

							}

					})
					.on('resize.sidebar-lock', function() {

						// Calculate heights.
							wh = $window.height();
							sh = $sidebar_inner.outerHeight() + 30;

						// Trigger scroll.
							$window.trigger('scroll.sidebar-lock');

					})
					.trigger('resize.sidebar-lock');

				});

	// Menu.
		var $menu = $('#menu'),
			$menu_openers = $menu.children('ul').find('.opener');

		// Openers.
			$menu_openers.each(function() {

				var $this = $(this);

				$this.on('click', function(event) {

					// Prevent default.
						event.preventDefault();

					// Toggle this opener.
						$this.toggleClass('active');

					// Close other openers only if they are not ancestors of this one (so parent menus stay open).
						$menu_openers.not($this).each(function() {
							var $op = $(this);
							if ($op.next('ul').has($this).length)
								return;
							$op.removeClass('active');
						});

					// Trigger resize (sidebar lock).
						$window.triggerHandler('resize.sidebar-lock');

				});

			});

})(jQuery);

// Keyboard shortcuts for flashcards
document.addEventListener('keydown', function(e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;

    var card = document.querySelector('.flashcard');
    if (!card) return;

    if (e.code === 'Space') {
        e.preventDefault();
        var btn = card.querySelector('button');
        var visible = card.classList.toggle('show-answer');
        if (btn) btn.textContent = visible ? 'Cacher la réponse' : 'Voir la réponse';
    } else if (e.code === 'ArrowRight') {
        e.preventDefault();
        var ok = card.querySelector('.check-icon');
        if (ok) ok.click();
    } else if (e.code === 'ArrowLeft') {
        e.preventDefault();
        var ko = card.querySelector('.cross-icon');
        if (ko) ko.click();
    }
});
// Inject search bar and enable filtering of menu courses
document.addEventListener('DOMContentLoaded', function() {
  var sidebarInner = document.querySelector('#sidebar .inner');
  if (sidebarInner && !document.getElementById('search')) {
    var section = document.createElement('section');
    section.id = 'search';
    section.className = 'alt';
    section.innerHTML = '<form method="post" action="#"><input type="text" name="query" id="query" placeholder="Rechercher"></form>';
    sidebarInner.insertBefore(section, sidebarInner.firstChild);
  }

  var input = document.querySelector('#sidebar #query');
  var menu = document.getElementById('menu');
  if (!input || !menu) return;

  var openers = menu.querySelectorAll('span.opener');
  input.addEventListener('input', function() {
    var q = input.value.toLowerCase().trim();
    // Filter links
    menu.querySelectorAll('li').forEach(function(li) {
      if (li.querySelector('.opener')) return;
      var link = li.querySelector('a');
      if (!link) return;
      var match = link.textContent.toLowerCase().includes(q);
      li.style.display = q === '' || match ? '' : 'none';
    });
    // Update categories
    openers.forEach(function(opener) {
      var sub = opener.nextElementSibling;
      if (!sub) return;
      var visible = q === '' || sub.querySelector('li:not([style*="display: none"])');
      opener.parentElement.style.display = visible ? '' : 'none';
      if (q === '') {
        opener.classList.remove('active');
        sub.style.display = '';
      } else if (visible) {
        opener.classList.add('active');
        sub.style.display = '';
      } else {
        opener.classList.remove('active');
        sub.style.display = 'none';
      }
    });
  });
});

// Add blue check icons in the menu for completed courses
document.addEventListener('DOMContentLoaded', function() {
  var links = document.querySelectorAll('#menu a[href$=".html"]');
  links.forEach(function(link) {
    var href = link.getAttribute('href');
    if (!href) return;
    var filename = href.split('/').pop().replace(/\.html$/, '');
    var key = 'completed_' + filename;
    if (localStorage.getItem(key) && !link.querySelector('.fa-check')) {
      var icon = document.createElement('span');
      icon.className = 'icon solid fa-check';
      icon.style.color = '#00aeef';
      icon.style.marginLeft = '0.25em';
      link.appendChild(icon);
    }
  });
});
