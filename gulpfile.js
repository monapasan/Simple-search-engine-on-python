'use strict';

// requirements

var gulp = require('gulp'),
    browserify = require('gulp-browserify'),
    size = require('gulp-size'),
    clean = require('gulp-clean');


// tasks
var path = './web/static/scripts/';
gulp.task('transform', function () {
  return gulp.src(path + 'jsx/main.js')
    .pipe(browserify({transform: ['reactify']}))
    .pipe(gulp.dest(path + 'js'))
    .pipe(size());
});
gulp.task('clean', function () {
  return gulp.src([path + 'js'], {read: false})
    .pipe(clean());
});
gulp.task('watch', function(){
    gulp.watch(path + 'jsx/main.js', ['transform']);
});
gulp.task('default', ['clean'], function() {
  gulp.start('transform');
});
