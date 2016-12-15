import re

# emails = ["itunespreview_en@2x.png","lt-wordmark-2013@2x.png"]

emails = ["issue-labelled-three-shot@2x.png",
"rails-rails-issues-three-shot@2x.png",
"windows-client@2x.png",
"rails-rails-compare-view-highlighted@2x.png",
"mac-client@2x.png",
"commit-issue-ref-three-shot@2x.png",
"twbs-bootstrap-milestones-three-shot@2x.png",
"jquery-jquery-pull-highlighted@2x.png",
"team-mention-screenshot@2x.png",
"3d-octocat@2x.jpg",
"svn-logo@2x.png",
"mobile-view@2x.png",
"label-editor-three-shot@2x.png",
"geojson@2x.jpg",
"commit-comment-highlighted@2x.png",
"etsy@2x-e186be5abd8b0f9181e4f12f159b47d6.png",
"vimeo@2x-f612c76a05288022433030201f5798ff.png",
"uofminnesota@2x-0d587589237ea7f7f88b760b8aceaa29.png",
"rackspace@2x-d52a068fcfd0fdbcf48eae6af4e2fda5.png",
"sap@2x-eb550d034fcc0ff10a63ac2b010624ef.png",
"paypal@2x-e709475f05e16f7dad2497cab18b663d.png",
"gree@2x-457ddfccfe5fdb8923479d3837631cd9.png",
"dena@2x-beec70913f011f834bda8a99049880e1.pngt"]

for email in emails:
	if re.match(r'([-\w@]+\.(?:jpg|gif|png))', email, flags=0):
	    print("matched %s" % email)
	else:
	    print("notmatched %s" % email)