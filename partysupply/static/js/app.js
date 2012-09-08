var InstagramPostView = Backbone.View.extend({
  tagName: "section",
  className: "instagram post",
  template: _.template($("#instagram-post-view").html()),

  render: function () {
    var that = this;
    this.$el.html(this.template({
      media: this.options.media,
      isodate: (new Date(parseInt(this.options.media.created_time, 10) * 1000)).toISOString()
    }));
    this.$el.hide();
    this.$(".image")
      .load(function () {
        _.defer(function () { that.$el.fadeIn(); });
        that.trigger("ready");
      })
      .attr("src", this.options.media.images.standard_resolution.url);
    this.$(".timestamp").timeago();
    return this;
  }

});

$(function () {
  var count = 0;

  _.each(BOOTSTRAP_DATA, function (media) {
    var view = new InstagramPostView({ media: media });
    setTimeout(function () { view.render().$el.prependTo(".posts"); }, (++count) * 350);
  });
  
});
