def activation_code_js_validator() -> str:
    # create the JS function to match activation code, abstracted out to allow for easier unit testing
    return """<script>
    function check_code(){
        var code = document.getElementById("input_code").value;
        if (code == "OCTOCAT") {
            window.location = "/register-user"
        }
        else {
            alert('Incorrect code');
        }
    }
    </script>"""
