/* sbflist.js */
function is_any_row_checked() {
	return $('.sbf-row :checkbox:checked').toArray().length > 0;
}

function check_all_rows(checked) {
	$('.rowcheck').each(function() {
		$(this).prop('checked', checked);
	});
}

function enable_row_buttons(checked) {
	$('.rowcheck-btn-group').each(function() {
		var btn = $(this);
		if (checked) {
			btn.removeClass('disabled');
		} else {
			btn.addClass('disabled');
		}
	});
}
/* filters */
var set_public_profile = function() {
	// get DB profile
	if (!localStorage.hasOwnProperty('public_profile')) return;
	var public_profile = JSON.parse(localStorage.public_profile);
	var profile = ProfileSettings;
	var profile_name = public_profile.name;
	profile.init(public_profile);
};

var set_profile_from_server = function()
{
	var ref_ps = "#sbf_profile-settings";
	if ($(ref_ps).data('custom_profile_settings')) {
		var settings = $(ref_ps).data('custom_profile_settings');
		var profile = ProfileSettings;
		if ($.isEmptyObject(settings) === true) {
			profile.setPublicSBF();
		} else {
			profile.setCustomSBF(settings, true);
		}
	}
};

/* SBF interface */
//UI control
var SBF = {

	SBFLIST_CONFIG_BTN: "#sbflist_config_btn",
	SBFLIST_FILTER_REM_BTN: "#sbflist_filter_rem_btn",

	show_profile:function()
	{
		/* config_btn sbf list */
		if (ProfileSettings.name_SBF() === 'custom') {
			$(SBF.SBFLIST_CONFIG_BTN).addClass("btn-warning").removeClass("btn-default");
			$(SBF.SBFLIST_FILTER_REM_BTN).addClass("btn-warning").removeClass("btn-default");
		} else {
			$(SBF.SBFLIST_CONFIG_BTN).removeClass("btn-warning").addClass("btn-default");
			$(SBF.SBFLIST_FILTER_REM_BTN).addClass("btn-default").removeClass("btn-warning");
		}
		this.hide_show_columns();
		this.set_input_filters();
		this.set_sorters();
	},
	hide_show_columns:function()
	{
		var rows = $(this.TABLE + ' th, ' + this.TABLE + ' td');
		rows.each(function() {
			var name = $(this).attr('name');
			if (name) {
				var current_profile = ProfileSettings.SBF();
				if (current_profile && current_profile.hasOwnProperty(name)) {
					var visible = current_profile[name].visible;
					visible === true ? $(this).removeClass('hide-column') : $(this).addClass('hide-column'); //jshint ignore:line
				}
			}
		});
	},
	set_input_filters:function()
	{
		var rows = $(this.TABLE + " [name='filters-row'] th");

		var colorize_object = function(name, input) {
			if (name) {
				var current_profile = ProfileSettings.SBF();
				if (current_profile && current_profile.hasOwnProperty(name)) {
					if (!current_profile[name].hasOwnProperty('filter')) {
						$(input).css("background-color", "#ffffff");
						return true; // continue
					}
					var text = current_profile[name].filter;
					text = $.trim(text);
					if (!text || text === '') {
						$(input).css("background-color", "#ffffff");
						return true;
					}
					$(input).val(text);
					$(input).css("background-color", "#eea236");
				}
			}
		};

		rows.each(function() {
			var name = $(this).attr('name');
			var input = $(this).find('input, select');
			colorize_object(name, input);
		});

		// fields outside SBF table
		colorize_object('technicians_contact_name:map:project', $("#sbflist_profile_technicians_contact_name"));


	},
	set_sorters:function()
	{
		var set_sorters = ProfileSettings.get_asc_desc_set_sorters_SBF();
		var ascs = set_sorters.asc;
		var descs = set_sorters.desc;
		var ref_sorter_cm = this.switch_sorter_context_menu;
		// remove sorters everywhere
		$(this.TABLE+' .sort-submitval>span').removeClass(this.ASC).removeClass(this.DESC);
		ref_sorter_cm($(this.TABLE+' .sort-submitval>span'), false); // remove context menu

		for (var i = 0; i < ascs.length; i++) {
			var sorter_asc = ascs[i];
			var sa = $(this.TABLE+' .sort-submitval[data-sort="'+sorter_asc+'"]' ).find('span');
			sa.addClass(this.ASC).css("background-color", "#eea236");
			ref_sorter_cm(sa, true); //add context menu
		}
		for (i = 0; i < descs.length; i++) {
			var sorter_desc = descs[i];
			var sd = $(this.TABLE+' .sort-submitval[data-sort="'+sorter_desc+'"]' ).find('span');
			sd.addClass(this.DESC).css("background-color", "#eea236");
			ref_sorter_cm(sd, true); //add context menu
		}
	},
	/* input change -> save to private profile */
	set_column_to_model:function(input) {
		var value = $.trim($(input).val());
		var unset = false;
		if (value.length === 0) unset = true;
		else unset=false;

		var name = ($(input).attr('name')).replace('filter_','');
		if (name.match(":int$")) {
			name = name.replace(":int","");
			var stripped = value.replace(/[^0-9]/g,'');
			value = parseInt(stripped);
			if (value > Number.MAX_SAFE_INTEGER || value < 0 || isNaN(value)) {
				unset = true;
			}
		}
		if (name.match(":date$")) {
			name = name.replace(":date","");
			value = value; //TODO create datetime
			// new Date("13-01-2011".replace( /(\d{2})-(\d{2})-(\d{4})/, "$2/$1/$3"));
		}
		if (name.match(":bool$")) {
			name = name.replace(":bool","");
			value = (value === 'true');
		}

		var profile = ProfileSettings;
		var user_profile = profile.get_custom_SBF();
		if (user_profile.hasOwnProperty('custom')) user_profile = user_profile.custom;
		if (!user_profile.hasOwnProperty(name)) return false;
		if (unset === false)  {
			user_profile[name]['filter'] = value;
		} else {
			if (user_profile[name].hasOwnProperty('filter'))
				delete user_profile[name]['filter'];
		}
		// set custom profile
		ProfileSettings.setCustomSBF({'custom': user_profile}, true);
		return user_profile;
	},
	set_sorter_to_model:function(name, sorting_option) {
		var profile = ProfileSettings;
		var user_profile = profile.get_custom_SBF();
		if (!user_profile.hasOwnProperty(name)) return false;
		if (!user_profile[name].hasOwnProperty('sort')) return false;
		user_profile[name].sort= sorting_option;
		ProfileSettings.setCustomSBF({'custom': user_profile}, true);
	},
	toggleSorter:function(sorter) {
		span = $(sorter).find('span');
		name = $(sorter).attr('data-sort');
		if (span.hasClass(this.DESC)) {
			span.removeClass(this.DESC).addClass(this.ASC);
			this.set_sorter_to_model(name, 'asc');
		} else
		{
			span.removeClass(this.ASC).addClass(this.DESC);
			this.set_sorter_to_model(name, 'desc');
		}
		this.switch_sorter_context_menu(span, true); // add context menu
	},
	clearSorter:function(th_sorter) {
		span = $(th_sorter).find('span');
		name = $(th_sorter).attr('name');
		if (name) {
			this.set_sorter_to_model(name, 'none');
			span.removeClass(this.ASC).removeClass(this.DESC);
			this.switch_sorter_context_menu(span, false); // remove context menu
		}
	},
	/* style sorter clear */
	switch_sorter_context_menu:function(span_sorter, turn)
	{
		(turn === true) ? span_sorter.addClass("context-menu-sort").addClass("sortup") : span_sorter.removeClass("context-menu-sort").removeClass("sortup");
	},
	TABLE:"#sbflist_table",
	ASC:"glyphicon-sort-by-attributes",
	DESC:"glyphicon-sort-by-attributes-alt"
};


/* main */
$(document).ready(function() {

	var checked = is_any_row_checked();
	enable_row_buttons(checked);
	$('.rowcheck-all').on('click', function() {
		var checked = $(this).prop('checked');
		check_all_rows(checked);
		enable_row_buttons(checked);
	});
	$('.rowcheck').on('click', function() {
		var checked = is_any_row_checked();
		enable_row_buttons(checked);
	});
	$('.rowcheck-btn').on('click', function(e) {
		e.preventDefault();
		var sbfids = [];
		$('.rowcheck').each(function() {
			var $this = $(this);
			if ($this.prop('checked') === true)
				sbfids.push($this.data('sbfid'));
		});
		var href = $(this).prop('href');
		if (sbfids.length > 0) {
			for (var i = 0; i < sbfids.length; ++i)
				href += '&sbfid[]=' + sbfids[i];
			$('.sbf-busy').show();
			$('#waitmodal').modal('show');
			document.location = href;
		}
	});
	$('#GSNBuildCompletedButton').on('click', function(e) {
		e.preventDefault();
		var sbfids = [];
		$('.rowcheck').each(function() {
			var $this = $(this);
			if ($this.prop('checked') === true)
				sbfids.push($this.data('sbfid'));
		});
		var href = $(this).data('href');
		if (sbfids.length > 0) {
			for (var i = 0; i < sbfids.length; ++i)
				href += '&sbfid[]=' + sbfids[i];
		}
		if ($('#delayed_why').val() !== '')
			href += '&delayed_why=' + $('#delayed_why').val();
		if ($('#workstart').val() !== '')
			href += '&workstart=' + $('#workstart').val();
		$('.sbf-busy').show();
		$('#waitmodal').modal('show');
		document.location = href;
	});

	//initialize filters
	set_public_profile();
	set_profile_from_server();

	SBF.show_profile();

	$('.filterableval').each(function() {
		var width = $(this).closest('th').width();
		$(this).show();
		$(this).closest('th').width(width);
	});

	// sbflist on sort action
	function sbflist_sort()
	{
		//$("span.glyphicon-sort, .filterableval").css("cursor", "progress").unbind("click");

		var SBF_array_profile = ProfileSettings.get_custom_SBF();
		if (SBF_array_profile === false) return;
		var href = window.location.href;
		$.ajax({
			type: 'POST',
			url: "/sbflist_sort",
			contentType: 'application/json;charset=UTF-8',
			async: true,
			data: JSON.stringify({'columns': SBF_array_profile}),
			})
			.done(function() {
					window.location.href=href;
			})
			.fail(function(err) {
			})
			.always(function() {
			//	$("span.glyphicon-sort, .filterableval").css("cursor", "default").bind("click");
			});
	}
	/* == events == */
	/* = get input from filter - input */
	$("input[name^='filter_']").on('keydown',function(e) {
		if (e.which == 13) {
			var target = $(e.target);
			if (target.hasClass('filterableval') || target.hasClass('sort-btn')) {
				e.stopPropagation();
				e.preventDefault();

				//$("span.glyphicon-sort, .filterableval").css("cursor", "progress").unbind("click");
				var url_current = window.location.href;

				var SBF_array_profile = SBF.set_column_to_model($(this));
				if (SBF_array_profile === false) return;
				$.ajax({
				type: 'POST',
				url: "/sbflist_config",
				contentType: 'application/json;charset=UTF-8',
				async: true,
				data: JSON.stringify({'columns': SBF_array_profile}),
				})
				.done(function() {
					  window.location.href=url_current;
				})
				.fail(function(err) {
					console.log(err.Message);
				})
				.always(function() {
				//	$("span.glyphicon-sort, .filterableval").css("cursor", "default").bind("click");
				});
			}
			else {
				return false;
			}
		}
	});

	/* = get input from filter - select */
	$("select[name^='filter_']").on('change',function(e) {
		e.stopPropagation();
		e.preventDefault();
		var url_current = window.location.href;

		//$("span.glyphicon-sort, .filterableval").css("cursor", "progress").unbind("click");

		var SBF_array_profile = SBF.set_column_to_model($(this));
		if (SBF_array_profile === false) return;
		$.ajax({
				type: 'POST',
				url: "/sbflist_config",
				contentType: 'application/json;charset=UTF-8',
				async: true,
				data: JSON.stringify({'columns': SBF_array_profile}),
				})
				.done(function() {
					  window.location.href=url_current;
				})
				.fail(function(err) {
				})
				.always(function() {
					//$("span.glyphicon-sort, .filterableval").css("cursor", "default").bind("click");
		});
	});

	/* are_date calendar */
	$('#filter_aredate').on('change', function()
	{
		var SBF_array_profile = SBF.set_column_to_model($(this));
		if (SBF_array_profile === false) return;

		var e = $.Event("keydown");
		e.which = 13;
		$("input[name^='filter__id']").trigger(e);
	});

	/* delayed_why field */
	$('#filter_delayed_why').on('change', function()
	{
		var SBF_array_profile = SBF.set_column_to_model($(this));
		if (SBF_array_profile === false) return;

		var e = $.Event("keydown");
		e.which = 13;
		$("input[name^='filter__id']").trigger(e);
	});

	/* clear current input field */
	$(SBF.TABLE+ ' .filter-rem-profile-btn').add('.sbf.filter-rem-profile-btn').click(function(event) {
		event.preventDefault();
		var input = $(this).prev();
		input.val('');
		$(input).css("background-color", "#ffffff");

		var e = $.Event("keydown");
		e.which = 13;
		e.target = $(input);
		$(input).trigger(e);
	});

	/* = clear filter = */
	$(SBF.SBFLIST_FILTER_REM_BTN).click(function(event) {
		event.stopPropagation();
		//$("span.glyphicon-sort, .filterableval").css("cursor", "progress").unbind("click");
		var url_current = window.location.href;

		(function() {
			$.post('/sbf_set_profile', { 'profile_name': "public" },
				function(returnedData){
					console.log(returnedData);
			}).fail(function(err){
				console.log(err.Message);
			}).done(function(evt) {
				console.log(evt);
			}).always(function() {
			//	$("span.glyphicon-sort, .filterableval").css("cursor", "default").bind("click");
				window.location.href=url_current;
			});
		})();
	});

	/* = click on sorters = */
	$(SBF.TABLE + " .sort-submitval").on('click', function() {
		SBF.toggleSorter($(this));

		// remove sorting on other elementsvar element = $(this).closest('th').attr('name');
		var other = $(this).closest("th").siblings().find("span[class*='glyphicon-sort-by-attributes']");
		for (var i = 0; i < other.length; i++) {
			SBF.clearSorter($(other[i]).closest("th"));
		}
		sbflist_sort();
	});

	$(SBF.SBFLIST_CONFIG_BTN).on('click', function() {
		//$("span.glyphicon-sort, .filterableval").css("cursor", "progress").unbind("click");
		// get
		$.ajax({
				type: 'GET',
				url: "/sbflist_config",
				contentType: 'application/json;charset=UTF-8',
				async: true
		})
		.done(function(evt) {
			// get only SBF list, either evt.public.* or evt.custom.*
			if (evt.hasOwnProperty('custom'))
			{
				ProfileSettings.setProfileSBF(evt);
			} else {
				ProfileSettings.setPublicSBF();
			}
			SBF_CONFIG.write_html();
		})
		.fail(function() {
		})
		.always(function() {
		//	$("span.glyphicon-sort, .filterableval").css("cursor", "default").bind("click");
		});
	});

	/* context menu */
	$.contextMenu({
		selector: '.context-menu-sort',
		zIndex: 10,
		callback: function(key) {
			var element = $(this).closest('th').attr('name');
			if (element) {
				SBF.set_sorter_to_model(element, "none");
				var e = $.Event("keydown");
				e.which = 13;
				$("input[name^='filter__id']").trigger(e);
			}
		},
		items: {
			"clear_sorting": { name: "Clear Sorting", icon: "delete"}
		}
	});

	/* delete sbf-list custom profile */
	$("#sbf_profile_remove_custom_profile_btn").on('click', function(e) {
		e.preventDefault();
		$('#waitmodal').modal('show');
		var href = $(this).data('href');
		document.location = href;
	});

	/* disabled add-sbf functionality in case disabled */
	$("#add_sbf_btn").on('click', function(ev) {
		if ($(ev.target).attr('disabled')) {
			ev.stopPropagation();
			return false;
		}
	});

	/* disabled add-sbf functionality in case disabled */
	$("#add_sbf_btn").on('click', function(ev) {
		if ($(ev.target).attr('disabled')) {
			ev.stopPropagation();
			return false;
		}
	});

	$('#btnAddService').on('click', function(ev) {
		$('#modalGSNService').modal('show');

		var $serviceSearchResult = $('#serviceSearchResult');
		var $addButton = $('#projectGSNServiceBtn');
		var $msgNotFound = $('#gsn-service-no-service-found-span');

		$serviceSearchResult.empty();

		var url = window.location.href;
		var projectIdRegex = /projectid=(\d+)/g;
		var match = projectIdRegex.exec(url);
		if (match) {
			var ajax_url = '/_ajax/search/GSN/impacted-service'
			var projectId = match[1];

			$('.sbf-busy').show();
			$('#waitmodal').modal('show');
			$.ajax({
					type: "GET",
					accepts: "application/json",
					url: ajax_url,
					data: {
						'project_id': projectId
					}
			}).done(function(data) {
				for (var i = 0; i < data.result.length; ++i) {
					var option = $('<option>').attr({
						value: data.result[i].name
					});
					var short_desc = data.result[i].short_description;
					if (!short_desc) short_desc = "";
					option.html(data.result[i].name + ': "' + short_desc.substr(0, 256) + '"');
					option.appendTo($serviceSearchResult);
				}

				if (data.result.length > 0) {
					$addButton.prop('disabled', false);
					$msgNotFound.hide();
				} else {
					$addButton.prop('disabled', true);
					$msgNotFound.show();
				}
			}).fail(function(e){
				console.error('Error handler...');
			}).always(function() {
				$('.sbf-busy').hide();
				$('#waitmodal').modal('hide');
			});
		} else {
			console.warn('Could not extract project id from URL');
		}
	});

	$('#projectGSNServiceBtn').on("click", function(e) {
		var selectedService = $('#serviceSearchResult').find('option:selected').val();
		console.info(selectedService);
		var selectedSBFs = $('.sbf-row :checkbox:checked').map(function(){return $(this).attr('data-sbfid')}).toArray();
		console.info(selectedSBFs);
		var selectedSBFsList = selectedSBFs.join(',');

		var ajax_url = '/_ajax/SBF/service/add';

		$('.sbf-busy').show();
		$('#waitmodal').modal('show');
		$.ajax({
				type: "POST",
				accepts: "application/json",
				url: ajax_url,
				data: {
				 	'selectedService': selectedService,
				 	'selectedSBFs': selectedSBFsList
				}
		}).done(function(data) {
			$('#modalGSNService').modal('hide');
		}).fail(function(e){
			console.error('Error handler...');
		}).always(function() {
			$('.sbf-busy').hide();
			$('#waitmodal').modal('hide');
		});
	});
});
