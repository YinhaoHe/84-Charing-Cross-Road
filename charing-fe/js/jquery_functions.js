/**
 * Created by Administrator on 2017/2/22.
 */
(function () {
    'use strict';
    var $button = $('#send-button');

    var charing = {};
    window.charing = charing;

    function isEmail(str){
        var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
        return reg.test(str);
    }

    function validatorState(obj,success) {
        if(success){
            obj.parent().removeClass('has-error has-warning').addClass('has-success');
            obj.parent().children('span').removeClass('glyphicon-remove glyphicon-warning-sign').addClass('glyphicon-ok');
        }else{
            obj.parent().removeClass('has-success has-warning').addClass('has-error');
            obj.parent().children('span').removeClass('glyphicon-ok glyphicon-warning-sign').addClass('glyphicon-remove');
        }
    };

    function validate() {
        var $first_mail_content = $('#first_mail_content');
        var $email = $('#email');
        var $sex = $('#sex');

        var errMsg = '';

        if($first_mail_content.val().length < 5){
            //为空
            validatorState($first_mail_content, false);
            if(errMsg===''){
                errMsg = '邮件内容太短';
            }
        }else {
            validatorState($first_mail_content, true);
        }

        if($email.val() === '' || !isEmail($email.val())){
            //为空
            validatorState($email, false);
            if(errMsg===''){
                errMsg = '邮箱未填或格式不正确';
            }
        }else {
            validatorState($email, true);
        }

        if($sex.val() !== '男' && $sex.val() !== '女'){
            //为空
            validatorState($sex, false);
            if(errMsg===''){
                errMsg = '性别未选择';
            }
        }else {
            validatorState($sex, true);
        }

        return errMsg;
    }

    function return_to_send_button(){
        //返回功能
        $('.fa').removeClass('fa-remove fa-check');
        $('#button-wrapper').removeClass('fail success clicked');
        $button.bind('click', on_send_button_click);
    }

    function on_send_button_click() {

        $('.form-group span').css('display','block');//全部显示



        var validate_errMsg;

        if((validate_errMsg = validate())!==''){
            $('.modal-title').text("提交失败");
            $('.modal-body p').text(validate_errMsg);
            $('#modal-button').bind('click',return_to_send_button);
            $('#myModal').modal('show');//弹出模态对话框
            return;
        }

        var first_mail_content = $('#first_mail_content').val();
        var email = $('#email').val();
        var sex = $('#sex').val();

        function onSuccessUI(){
            $button.children('.fa').removeClass('fa-remove').addClass("fa-check");//设定成功
            $('#button-wrapper').addClass('success');

            $('.modal-title').text("提交成功");
            $('.modal-body p').text("恭喜您，提交成功！");

            $button.children('.fa').bind('click',function () {
                $('#modal-button').bind('click',return_to_send_button);
                $('#myModal').modal('show');
            });
        }
        function onFailUI(){
            $button.children('.fa').removeClass('fa-check').addClass("fa-remove");//设定成功
            $('#button-wrapper').addClass('fail');


            $('.modal-title').text("提交失败");
            if(charing.errmsg === "duplicate_email"){
                $('.modal-body p').text("您的邮箱已经在本站提交过了!");
            }else if(charing.errmsg === "db_error"){
                $('.modal-body p').text("服务器数据库故障，请联系站长");
            }else if(charing.errmsg === "sex_error"){
                $('.modal-body p').text("性别填写有误");
            }else if(charing.errmsg === "email_error"){
                $('.modal-body p').text("邮箱填写有误");
            }else{
                $('.modal-body p').text(charing.errmsg)
            }

            $button.children('.fa').bind('click',function () {
                $('#modal-button').bind('click',return_to_send_button);
                $('#myModal').modal('show');
            });
        }

        $(this).parent().addClass('clicked');

        $(this).unbind('click');//发送按钮发送一次就失效

        $.ajax({
            type:"post",
            url: "post",
            data: {
                first_mail_content: first_mail_content,
                email: email,
                sex: sex
            },
            success: function (data, status) {

                if (status === "success") {
                    var dataObject;
                    try {
                        dataObject = JSON.parse(data);
                        if (dataObject[0] === 'false') {
                            charing.errmsg = dataObject[1];
                            onFailUI();
                            return;
                        }
                    } catch (err) {
                        charing.errmsg = 'Unknown';
                        onFailUI();
                        return;
                    }
                    onSuccessUI();
                    return;
                } else {
                    charing.errmsg = status;
                    onFailUI();
                    return;
                }

            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                charing.errmsg = errorThrown;
                onFailUI();
                return;
            }

        });

    }

    $button.bind('click', on_send_button_click);

    $(".form-group textarea,input,select").bind('input propertychange', function() {
        $(this).parent().children('span').css('display','block');//只追加当前

        validate();
    });

    $('#help-button').bind('click',function () {
        $('.modal-title').text("帮助");
        $('.modal-body p').text("　　这里是一个在线版的查令十字街84号书店。我们会将向书店寄信的人配对，向书店寄的信会被自动转发给另一方。第一封信必须在网站上寄出，后续用自己的邮箱向charing84@hotmail.com寄信即可。期待在这里能够找到您的挚友~");
        $('#modal-button').unbind('click');//按钮点击事件置空
        $('#myModal').modal('show');//弹出模态对话框
    });


}());