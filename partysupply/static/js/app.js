var InstagramPost = Backbone.Model.extend({
  initialize: function () {
    this.set("created_time", new Date(parseInt(this.get("created_time"), 10) * 1000));
  }
});

var InstagramPostCollection = Backbone.Collection.extend({
  model: InstagramPost,

  url: function(){
    return "/posts?since=" + (posts.last().get("created_time").valueOf() / 1000);
  },

  comparator: function (post) {
    return post.get("created_time");
  }
})

var InstagramPostView = Backbone.View.extend({
  tagName: "section",
  className: "instagram post",
  template: _.template($("#instagram-post-view").html()),

  render: function () {
    var that = this;
    this.$el.html(this.template({
      media: this.model.toJSON(),
      isodate: this.model.get("created_time").toISOString()
    }));
    this.$el.hide();
    this.$(".image")
      .load(function () {
        _.defer(function () { that.$el.fadeIn(); });
        that.trigger("ready");
      })
      .attr("src", this.model.get("images").standard_resolution.url);
    this.$(".timestamp").timeago();
    return this;
  }

});

$(function () {
  var count = 0;

  // _.each(BOOTSTRAP_DATA, function (media) {
  //   var view = new InstagramPostView({ media: media });
  //   setTimeout(function () { view.render().$el.prependTo(".posts"); }, (++count) * 1000);
  // });
  
  window.posts = new InstagramPostCollection();
  
  posts.on("add", function (post) {
    var view = new InstagramPostView({ model: post });
    setTimeout(function () { view.render().$el.prependTo(".posts"); }, (++count) * 1000);
  });
  
  posts.add(BOOTSTRAP_DATA.posts);
});
