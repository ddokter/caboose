$(document).ready(function() {

  $(".listingfilter").on('keyup', function(e) {

    var li;
    var text = $(e.target).val().toLowerCase();
    var listing = $(e.target).parents(".listing").eq(0);

    //if(text.length < 3) {
    //  return false;
    //}

    if (!text) {
      listing.find(".list-group-item").show();
    } else {

      listing.find(".list-group-item").each(function(idx, elt) {

        li = $(elt);

        if (li.text().toLowerCase().indexOf(text) == -1) {
          li.hide();
        } else {
          li.show();
        }
      });
    }
  });

  $(".listingfilter").submit(function(e) {

    var form = $(e.target);
    var listing = form.parents(".listing").eq(0);
    var li;
    var text = form.find("[name=filter]").val().toLowerCase();

    if (!text) {
      listing.find(".list-group-item").show("slow");
    } else {

      listing.find(".list-group-item").each(function(idx, elt) {

        li = $(elt);

        if (li.text().toLowerCase().indexOf(text) == -1) {
          li.hide("slow");
        } else {
          li.show("slow");
        }
      });
    }

    e.preventDefault();

    return false;
  });

    $('select[name$="ingredient"]').each(function() {
	$(this).chosen({inherit_select_classes:true});
    });

    $('select[name="subs"]').each(function() {
	$(this).chosen({inherit_select_classes:true});
    });

    $('select[name="recipe"]').each(function() {
	$(this).chosen({inherit_select_classes:true});
    });
    
});
