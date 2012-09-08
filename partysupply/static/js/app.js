var InstagramPostView = Backbone.View.extend({
  tagName: "section",
  className: "instagram post",
  template: _.template($("#instagram-post-view").html()),

  render: function () {
    this.$el.html(this.template({
      media: this.options.media,
      isodate: (new Date(parseInt(this.options.media.created_time, 10) * 1000)).toISOString()
    }));
    this.$(".timestamp").timeago();
    return this;
  }

});

$(function () {
  
  _.each(BOOTSTRAP_DATA, function (media) {
    var view = new InstagramPostView({ media: media });
    view.render().$el.appendTo("#wrap");
  });
  
});