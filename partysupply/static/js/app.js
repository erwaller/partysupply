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
    if (app.posts.last()) {
      since = app.posts.last().get("created_time").valueOf() / 1000;
    }
    return "/posts?" + $.param({ "since": since });
  },

  comparator: function (post) {
    return post.get("created_time");
  },

  parse: function (response) {
    return response.posts
  },

  startPolling: function (period) {
    var that = this;
    period = period || (app.is_mobile ? 4000 : 2000);
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

var AppView = Backbone.View.extend({

  initialize: function () {
    this.is_mobile = window["screen"] && (screen.width < 480 || screen.height < 480);
    this.posts = new InstagramPostCollection();
    this.posts.on("add", function (post) {
      var view = new InstagramPostView({ model: post });
      view.render().$el.prependTo(".posts");
    });
  },

  render: function () {
    if (BigScreen.enabled) {
      $(document).keyup(function (e) {
        if (e.shiftKey && e.keyCode == 70) {
          BigScreen.toggle();
        }
      });
    }

    this.posts.add(BOOTSTRAP_DATA.posts);
    this.posts.startPolling();

    _.defer(function() {
      window.scrollTo(0, 0);
    });
  }

});

$(function () {
  window.app = new AppView();
  app.render();
});
