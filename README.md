- Các cách xác định
	+ Test từng port
	+ parse từ output command

- Công việc
	+ Xác định các port đang mở
	+ dịch vụ, thông tin chi tiết các dịch vụ trên các port mở

- Mục đích:
	+ Xác định được các dịch vụ đang chạy
	+ Thông tin các dịch vụ
		+ Locate các dịch vụ


- Kết nối client với server.
	Server gửi thông tin kết nối được mã hóa jwt bằng chính secret_code được cấu hình.



Generate config files,
	Tiết kiệm thời gian,
	Tạo file cấu hình tự động => sinh tự động cho các hệ thống cloud hoặc quản lý tự động

font for commands "droid-sans-mono",


#Phần quản lý người dùng:
    Có 2 quyền: member, manage

[Ruby]
# We support all major Ruby versions. Please see our documentation for a full list.
# https://documentation.codeship.com/basic/languages-frameworks/ruby/

# If `.ruby-version` file is present, RVM will set Ruby to the declared version.
if [ -f .ruby-version ]; then rvm use $(cat .ruby-version) --install; fi

# If you are not using a `.ruby-version` in your project,
# then the desired version of Ruby can be declared in the following manner:
# rvm use 2.2.3 --install

bundle install

[Ruby On Rails]
# We support all major Ruby versions. Please see our documentation for a full list.
# https://documentation.codeship.com/basic/languages-frameworks/ruby/

# If `.ruby-version` file is present, RVM will set Ruby to the declared version.
if [ -f .ruby-version ]; then rvm use $(cat .ruby-version) --install; fi

# If you are not using a `.ruby-version` in your project,
# then the desired version of Ruby can be declared in the following manner:
# rvm use 2.2.3 --install

bundle install

# Make sure Ruby on Rails knows we are in the the test environment.
export RAILS_ENV=test

# Prepare the test database
bundle exec rake db:schema:load
#bundle exec rake db:migrate
#bundle exec rake db:test:prepare

[NodeJS Meteor]
# We support all major Node.js versions. Please see our documentation for a full list.
# https://documentation.codeship.com/basic/languages-frameworks/nodejs/
#
# By default we use the Node.js version specified in your package.json file and fall
# back to the latest version from the 0.10 release branch.
#
# You can use nvm to install any Node.js version you require
#nvm install 0.10

# Meteors default installer requires sudo on Linux. We use a script to change install
# location and make sudo unecessary.
curl -sSL https://raw.githubusercontent.com/codeship/scripts/master/packages/meteor.sh | bash -s
meteor npm install
