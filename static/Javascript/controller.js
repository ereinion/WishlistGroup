var lister = angular.module('lister', []);

lister.controller('ChatController', function($scope)
{
    var socket = io.connect('https://' + document.domain + ':' 
    +location.port + '/lister'); 
    
    $scope.userData = [];
    $scope.friendData = [];
    
    $scope.register = function register()
    {
        if($scope.remail != "" && $scope.rpassword != "" && $scope.firstname != "" && $scope.lastname != "" && $scope.cpassword != "")
        {
            socket.emit('register', $scope.remail, $scope.rpassword, $scope.cpassword, $scope.firstname, $scope.lastname);
            $scope.remail = '';
            $scope.rpassword = '';
            $scope.firstname = '';
            $scope.lastname = '';
            $scope.cpassword = '';
            $scope.subed=false;
        }
        else
        {
            //print that an input is incomplete
        }
    };
    
    $scope.update = function update()
    {
        if($scope.most)
        {
            socket.emit('most', $scope.most);
            console.log(1);
        }

        if($scope.birth)
        {
            socket.emit('birth', $scope.birth);
            console.log(3);
        }
        if($scope.gender)
        {
            socket.emit('gender', $scope.gender);
            console.log(4);
        }
        if($scope.home)
        {
            socket.emit('home', $scope.home);
            console.log(5);
        }
        if($scope.number)
        {
            socket.emit('number', $scope.number);
            console.log(6);
        }
        socket.emit('getData');
    };
    
    $scope.setFriendData = function setFriendData(data)
    {
        socket.emit('getFriendData', data);
        console.log(data);
    };
    
    $scope.search = function search()
    {
        $scope.searchRes = [];
           $scope.results = $scope.searchFor;
           if($scope.searchFor == "")
           {
               document.getElementById("resultList").style.display = "none";
               document.getElementById("noResults").style.display = "block";
           }
           else
           {
                socket.emit('getResults', $scope.searchFor);
           }

    };
 
    $scope.sub = function sub(data)
    {
        console.log("yes!");
        socket.emit('subscribe', data);
        socket.emit('getFriendData', data);
        //socket.emit('getResults', data);
    };
    
    $scope.unsub = function unsub(data)
    {
        console.log("yes!");
        socket.emit('unsubscribe', data);
        socket.emit('getFriendData', data);
        //socket.emit('getResults', data);
        
    };
    
//-------------------------------------------------------
 
    socket.on('connect', function()
    {
        console.log('connected');
        socket.emit('getData');
    });
    
    socket.on('registersuccess', function()
    {
        console.log("success");
        document.getElementById("alert").innerHTML = "<div class='alert alert-success'>Account Created!</div>";
    });
    
    socket.on('registerfailure', function(reason)
    {
        console.log(reason);
        document.getElementById("alert").innerHTML = "<div class='alert alert-danger'>"+ reason +"</div>";
    });
    
     socket.on('setData', function(data)
    {
        $scope.userData = [];
        for(var i = 0; i < data.length; i++)
        {
            $scope.userData.push(data[i]);
            $scope.$apply();
            console.log(data[i]);
        }
    });
    
    socket.on('searchResults', function(data)
    {
        $scope.searchRes = [];
        for(var i = 0; i < data.length; i++)
        {
            $scope.searchRes.push(data[i]);
            $scope.$apply();
            console.log(data[i]);
        }
        
        if(data.length == 0)
        {
            document.getElementById("resultList").style.display = "none";
        }
        else
        {
            document.getElementById("resultList").style.display = "block";    
        }

    });
    
    socket.on('setFriendData', function(data)
    {
        console.log("test!");
        $scope.friendData = [];
        for(var i = 0; i < data.length; i++)
        {
            $scope.friendData.push(data[i]);
            $scope.$apply();
            console.log(data[i]);
            console.log($scope.friendData[i]);
        }
    });
});