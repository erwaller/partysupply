var InstagramPost = Backbone.Model.extend({
  initialize: function () {
    this.set("created_time", new Date(parseInt(this.get("created_time"), 10) * 1000));
  }
});

var InstagramPostCollection = Backbone.Collection.extend({
  model: InstagramPost,

  initialize: function () {
    this.polling_interval = null;
  },

  url: function(){
    var since = 0;
    if (posts.last()) {
      since = posts.last().get("created_time").valueOf() / 1000;
    }
    return "/posts?" + $.param({ "since": since, "_": (new Date()).valueOf() });
  },

  comparator: function (post) {
    return post.get("created_time");
  },

  parse: function (response) {
    return response.posts
  },

  startPolling: function (period) {
    var that = this;
    period = period || 2000;
    this.polling_interval = setInterval(function () {
      that.fetch({ add: true });
    }, period);
  },

  stopPolling: function () {
    clearInterval(this.polling_interval);
    this.polling_interval = null;
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
        _.defer(function () {
          that.$el
            .addClass("fade-in")
            .show();
        });
        that.trigger("ready");
      })
      .attr("src", this.model.get("images").standard_resolution.url);
    this.$(".timestamp").timeago();
    return this;
  }

});

$(function () {
  $(document).keyup(function (e) {
    if (e.shiftKey && e.keyCode == 70) {
      if (BigScreen.enabled) {
        BigScreen.toggle();
      } else {
        // fallback for browsers that don't support full screen
      }
    }
  });

  window.posts = new InstagramPostCollection();
  posts.on("add", function (post) {
    var view = new InstagramPostView({ model: post });
    view.render().$el.prependTo(".posts");
  });
  posts.add(BOOTSTRAP_DATA.posts);
  posts.startPolling();


  _.defer(function() {
    window.scrollTo(0, 0);
  });
});
