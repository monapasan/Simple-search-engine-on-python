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
          var command;
          if(searchString.indexOf(':') === 0){
              command = searchString.split(':')[1].toLowerCase();
              this.handleCommandSearch(command);
          } else {
              this.setState({command: false});
              this.handleSubmit({'query': searchString});
          }
      },
      handleCommandSearch: function(command){
          var commands = {
              'getlength': true,
              'getlinkstruktur': true,
              'getpagerank': true
          };
          if(!commands[command])
              this.setState({commandResults: false});
          else
              this.handleSubmit({command: command});
          this.setState({command: command});
      },
      handleSubmit: function (data) {
          $.ajax({
              type: "POST",
              url: '/',
              data: data,
              success: this.successQuery,
              error: function (xhr, status, err) {
                  console.error( status, err.toString());
              }.bind(this)
          });
      },
      successQuery:function(data){
          if(this.state.command){
              this.setState({commandResults: data});
              console.log(data);
          }else{
              this.setState({searchResults: data});
          }
      },
      renderSearchResults:function(){
          var withRanking = [];
          var cosineScore = [];
          var pageRank = [];
          // TODO: What the fuck !? Change in python!!
          var linkPath = 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/';
          if(this.state.searchResults){
              withRanking = this.state.searchResults.WithRanking;
              cosineScore = this.state.searchResults.CosineScore;
              pageRank = this.state.searchResults.PageRank;
          }
          cosineScoreObj = {};
          cosineScore.map(function(val){
              cosineScoreObj[val[0]] = val[1];
          });
         return( React.createElement("ul", null, 
            withRanking.map(function(res, i){
                return React.createElement("li", null, React.createElement("div", {className: "res-name"}, React.createElement("a", {target: "_blank", href: linkPath + res[0]}, res[0])), 
                  React.createElement("div", {className: "res-score"}, 
                      React.createElement("p", null, "Score with withRanking :", React.createElement("span", {className: "score-value"}, " ", res[1])), 
                      React.createElement("p", null, "PageRank : ", React.createElement("span", {className: "score-value"}, pageRank[res[0]])), 
                      React.createElement("p", null, "CosineScore : ", React.createElement("span", {className: "score-value"}, cosineScoreObj[res[0]]))
                  )
                  );
            })
          ));
      },
      renderCommandResults: function(){
          var data = this.state.commandResults;
          if(!data){
              return (React.createElement("h3", null, "Wrong command!"));
          } else if (this.state.command === 'getlinkstruktur'){
              return this.renderPageRankResults(data, true);
          } else {
              return this.renderPageRankResults(data);
          }
      },
      renderPageRankResults:function(data, linkStructure){
          var dataArr = [];
          if(linkStructure === true){
              for(var i in data){
                var str = "";
                for(var link in data[i])
                    str += link + " ";
                dataArr.push([i,str]);
              }
          }
          else {
              for(var key in data)
                  dataArr.push([key,data[key]]);
          }
          return(React.createElement("ul", {className: "pagerank"}, 
              dataArr.map(function(val){
                  return React.createElement("li", null, val[0], " : ", React.createElement("div", {className: "pagerankval"}, val[1]));
              })
          ));
      },
      showResults:function(){
          if(this.state.command)
              return this.renderCommandResults();
          else if (this.state.searchResults)
              return this.renderSearchResults();
      },
      render: function() {

        var searchString = this.state.searchString.trim().toLowerCase();

        return (
          React.createElement("div", null, 
            React.createElement("input", {type: "text", value: this.state.searchString, onChange: this.handleChange, placeholder: "Search!"}), 
            React.createElement("button", {className: "search-button", onClick: this.handleSearch}, " Search "), 
            this.showResults()
          )
      );
      }

    });

    React.render(
      React.createElement(DynamicSearch, null),
      document.getElementById('main')
    );


},{}]},{},[1])