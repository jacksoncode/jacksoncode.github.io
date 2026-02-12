const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const browserSync = require('browser-sync').create();
const header = require('gulp-header');
const cleanCSS = require('gulp-clean-css');
const rename = require('gulp-rename');
const uglify = require('gulp-uglify');
const pkg = require('./package.json');

const banner = ['/*!\n',
    ' * Start Bootstrap - <%= pkg.title %> v<%= pkg.version %> (<%= pkg.homepage %>)\n',
    ' * Copyright 2013-' + (new Date()).getFullYear() + ' <%= pkg.author %>\n',
    ' * Licensed under <%= pkg.license.type %> (<%= pkg.license.url %>)\n',
    ' */\n',
    ''
].join('');

function sassTask() {
    return gulp.src('scss/clean-blog.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(header(banner, { pkg: pkg }))
        .pipe(gulp.dest('css'))
        .pipe(browserSync.reload({ stream: true }));
}

function minifyCss() {
    return gulp.src('css/clean-blog.css')
        .pipe(cleanCSS({ compatibility: 'ie9' }))
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest('css'))
        .pipe(browserSync.reload({ stream: true }));
}

function minifyJs() {
    return gulp.src('js/clean-blog.js')
        .pipe(uglify())
        .pipe(header(banner, { pkg: pkg }))
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest('js'))
        .pipe(browserSync.reload({ stream: true }));
}

function copy() {
    return gulp.src(['node_modules/bootstrap/dist/**/*', '!**/npm.js', '!**/bootstrap-theme.*', '!**/*.map'])
        .pipe(gulp.dest('lib/bootstrap'))

    gulp.src(['node_modules/jquery/dist/jquery.js', 'node_modules/jquery/dist/jquery.min.js'])
        .pipe(gulp.dest('lib/jquery'));

    return gulp.src(['node_modules/@fortawesome/fontawesome-free/**', '!node_modules/@fortawesome/fontawesome-free/**/*.map', '!node_modules/@fortawesome/fontawesome-free/.npmignore', '!node_modules/@fortawesome/fontawesome-free/*.txt', '!node_modules/@fortawesome/fontawesome-free/*.md', '!node_modules/@fortawesome/fontawesome-free/*.json'])
        .pipe(gulp.dest('lib/font-awesome'));
}

function browserSyncInit(done) {
    browserSync.init({
        server: { baseDir: '' }
    });
    done();
}

function watch() {
    gulp.watch('scss/*.scss', sassTask);
    gulp.watch('css/*.css', minifyCss);
    gulp.watch('js/*.js', minifyJs);
    gulp.watch('*.html').on('change', browserSync.reload);
}

const defaultTask = gulp.series(sassTask, minifyCss, minifyJs, copy);
const devTask = gulp.series(gulp.parallel(browserSyncInit, defaultTask), watch);

exports.default = defaultTask;
exports.dev = devTask;
exports.sass = sassTask;
exports.minifyCss = minifyCss;
exports.minifyJs = minifyJs;
exports.copy = copy;
