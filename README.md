# Todo

### Completed
- [x] users need to signup
- [x] users need to login
- [x] users need to logout
- [x] create a monster/npc
- [x] get monster/npc to show up next to the monster/npc list
- [x] implement bootstrap
- [x] CRUD campaign
- [x] CRUD chapter
- [x] CRUD section
- [x] re-order chapters
- [x] single-pane view with campaign/character list on left, content on right
- [x] BUG: messages 'x' won't close the message
- [x] CRUD monster
- [x] CRUD npc
- [x] change to CBV for monsters/npcs
- [x] BUG: fix success url when creating a chapter so that it goes to the current campaign and chapter
- [x] BUG: get rid of horizontal bar in campaigns if you don't have any campaigns
- [x] monster list should be alphabetical
- [x] center messages text
- [x] nest campaign sections under chapters
- [x] re-order sections
- [x] BUG: campaign when making a new chapter/section should be the current campaign
- [x] implement tinymce
- [x] put user's email in top spot of account dropdown
- [x] BUG: fix monster and npc links when blank
- [x] add success message after deleting campaign
- [x] auto-link to monsters/npcs in campaign
- [x] add navbar icons
- [x] add breadcrumbs to campaign title section
- [x] delete monster/npc success message
- [x] use "chapter number" instead of order, and then display in the contents list as roman numeral
- [x] BUG: fix alerts with breadcrumbs design
- [x] BUG: fix campaign with no chapters view
- [x] move css styles from inline to stylesheet
- [x] add 3rd party logins to signup
- [x] remove "successfully logged in" message
- [x] send email for verification during signup
- [x] style the login and signup pages
- [x] style verification email
- [x] check if "accounts" folder is still used, delete if not
- [x] migrate to new server
- [x] add favicon
- [x] bootstrap form styling
- [x] move "update" on CRUD pages to beginning
- [x] add cancel button to CRUD views
- [x] change cog hover color
- [x] [look into doing tinymce more proper](http://stackoverflow.com/questions/19013509/tinymce-widget-usage-in-django-template)
- [x] implement tinymce site-wide
- [x] style monster/npc CRUD
- [x] use get_object_or_404 on views
- [x] delete campaign view needs to be styled
- [x] check all titles and make sure they are using "title | super" format
- [x] consolidate campaign and campaign_update
- [x] add campaign to admin
- [x] add ability to order sections in chapter update similar to how you can order chapters in campaign update
- [x] use google mail servers instead of local mail server
- [x] style email verification page
- [x] remove settings.py from version control
- [x] create wiki
- [x] style admin login
- [x] fill wiki with content
- [x] style monster/npc page
- [x] users need to delete their account - should it be inactive or aaron hernandez?
- [x] profile page
- [x] need to be able to signup with facebook and link google afterwards
- [x] redo delete views so that they redirect better
- [x] password reset email styling
- [x] need to be able to reset password

### Site-wide
- [ ] write tests
- [ ] players
- [ ] home page (blog? tutorial?)

### Users
- [ ] need to be able to change email ([template](https://github.com/pennersr/django-allauth/blob/master/allauth/templates/account/email.html), [view](https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py), [url](https://github.com/pennersr/django-allauth/blob/master/allauth/account/urls.py))

### Campaign
- [ ] add option in "edit campaign" to drag/drop to change order of chapters, order number should auto-update as you do it

### Monsters/NPCs
- [ ] import monster/npc

### TinyMCE
- [ ] tinymce uploads ([tinymce](https://www.tinymce.com/docs/configure/file-image-upload/), [django](http://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example))
