source "https://rubygems.org"

# Jekyll core
gem "jekyll", "~> 4.3"

# Jekyll plugins
group :jekyll_plugins do
  gem "jekyll-sitemap"      # Automatic sitemap generation
  gem "jekyll-seo-tag"      # SEO meta tags
end

# Platform-specific gems
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance booster for watching directories
gem "wdm", "~> 0.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock http_parser.rb to v0.6.x for JRuby
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
