/** @jsx React.DOM */


    var DynamicSearch = React.createClass({

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
              'getpagerank': true,
              'getterms' : true
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
         return( <ul>
            {withRanking.map(function(res, i){
                return <li><div className="res-name"><a target="_blank" href={linkPath + res[0]}>{res[0]}</a></div>
                  <div className="res-score">
                      <p>Score with withRanking :<span className="score-value"> {res[1]}</span></p>
                      <p>PageRank : <span className="score-value">{pageRank[res[0]]}</span></p>
                      <p>CosineScore : <span className="score-value">{cosineScoreObj[res[0]]}</span></p>
                  </div>
                  </li>;
            })}
          </ul>);
      },
      renderCommandResults: function(){
          var data = this.state.commandResults;
          if(!data){
              return (<h3>Wrong command!</h3>);
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
          return(<ul className='pagerank'>
              {dataArr.map(function(val){
                  return <li>{val[0]} : <div className='pagerankval'>{val[1]}</div></li>;
              })}
          </ul>);
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
          <div>
            <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search!" />
            <button  className='search-button' onClick={this.handleSearch}> Search </button>
            {this.showResults()}
          </div>
      );
      }

    });

    React.render(
      <DynamicSearch  />,
      document.getElementById('main')
    );
