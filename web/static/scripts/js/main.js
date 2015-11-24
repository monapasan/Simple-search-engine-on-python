(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
/** @jsx React.DOM */

    var DynamicSearch = React.createClass({displayName: "DynamicSearch",

      // sets initial state
      getInitialState: function(){
        return { searchString: '' };
      },

      // sets state, triggers render method
      handleChange: function(event){
        // grab value form input box
        this.setState({searchString:event.target.value});
      },
      handleSearch:function(){
          var searchString = this.state.searchString.trim().toLowerCase();
          console.log(searchString);
          this.handleTaskSubmit(searchString);
      },
      handleTaskSubmit: function (searchString) {
          $.ajax({
              type: "POST",
              url: '/',
              data: {'query': searchString},
              success: this.successQuery,
              error: function (xhr, status, err) {
                  console.error( status, err.toString());
              }.bind(this)
          });
      },
      successQuery:function(data){
          this.setState({searchResults: data});
      },
      render: function() {

        var countries = this.props.items;
        var searchString = this.state.searchString.trim().toLowerCase();
        var WithRanking = [];
        var CosineScore = [];
        var PageRank = [];
        if(this.state.searchResults){
            WithRanking = this.state.searchResults.WithRanking;
            CosineScore = this.state.searchResults.CosineScore;
            PageRank = this.state.searchResults.PageRank;
        }
        //   { countries.map(function(country){ return <li>{country.name} </li>; }) }

        // filter countries list by value from input box
        if(searchString.length > 0){
          countries = countries.filter(function(country){
            return country.name.toLowerCase().match( searchString );
          });
        }
        return (
          React.createElement("div", null, 
            React.createElement("input", {type: "text", value: this.state.searchString, onChange: this.handleChange, placeholder: "Search!"}), 
            React.createElement("button", {onClick: this.handleSearch}, "My Button"), 
            React.createElement("ul", null, 
              WithRanking.map(function(res, i){
                  return React.createElement("li", null, res[0], 
                    React.createElement("p", null, "WithRanking : ", res[1]), 
                    React.createElement("p", null, "PageRank : ", PageRank[res[0]]), 
                    React.createElement("p", null, "CosineScore : ", CosineScore[i][1])
                    );
              })
            )
          )
      );
      }

    });

    // list of countries, defined with JavaScript object literals
    var countries = [
      {"name": "Sweden"}, {"name": "China"}, {"name": "Peru"}, {"name": "Czech Republic"},
      {"name": "Bolivia"}, {"name": "Latvia"}, {"name": "Samoa"}, {"name": "Armenia"},
      {"name": "Greenland"}, {"name": "Cuba"}, {"name": "Western Sahara"}, {"name": "Ethiopia"},
      {"name": "Malaysia"}, {"name": "Argentina"}, {"name": "Uganda"}, {"name": "Chile"},
      {"name": "Aruba"}, {"name": "Japan"}, {"name": "Trinidad and Tobago"}, {"name": "Italy"},
      {"name": "Cambodia"}, {"name": "Iceland"}, {"name": "Dominican Republic"}, {"name": "Turkey"},
      {"name": "Spain"}, {"name": "Poland"}, {"name": "Haiti"}
    ];

    React.render(
      React.createElement(DynamicSearch, {items:  countries }),
      document.getElementById('main')
    );


},{}]},{},[1])