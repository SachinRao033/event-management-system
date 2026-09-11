import {Link, useNavigate } from "react-router-dom";
import {useState} from "react";
import api from "../services/api.js";

export default function Login() {
    const navigate = useNavigate();

    // stores the local login form values
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    // Stores validation/backend error message
    const [error, setError] = useState("");

    // Stores loading state while login request is running
    const [loading, setLoading] = useState(false);

    function handleChange(e){
        const {name, value} = e.target;
        setFormData(prevData =>({
            ...prevData,
            [name]: value
        }));

        // Remove error when user starts typing again
        if (error) {
            setError("");
        }
        
    }

    

    // prevents page refresh until authentication is implemented
    const handleSignIn = async (e) =>{
        e.preventDefault();

        // clear previous error message
        setError("");

        // validation
        if(!formData.email.trim()) {
            setError("Please enter your email address.");
            return;
        }

        if(!formData.password) {
            setError("Please enter your password.");
            return;
        }

        setLoading(true);

        try{
            // username and password as form data
            const loginData = new URLSearchParams();
            loginData.append("username", formData.email);
            loginData.append("password", formData.password);

            // send login request to backend
            const res = await api.post("/auth/login", loginData, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            });

             // Save JWT token
             localStorage.setItem("token", res.data.access_token);

             // login successful
             navigate("/home");

        } catch(err) {
            console.error(err);

            // backend error message
            const message = err.response?.data?.detail || "Login failed. Please check your email and password.";
            setError(message);

        } finally {
            setLoading(false);
        }
    };


    return (
        <div className= "container min-vh-100 d-flex justify-content-center align-items-center">
            <div style={{background: "#EFF1F3", maxWidth: "600px"}} className="container-fluid d-flex flex-column justify-content-center align-items-center p-5 rounded-5">
                <i className="bi bi-calendar2-week fs-1 eventhub-color"></i>
                <h1 className="eventhub-color fw-bold">EventHub</h1>
                <p>Professional Event Management Portal</p>

                {/* Error message */}
                {error && (
                    <div className="alert alert-danger w-100" role="alert">
                        {error}
                    </div>
                )}

                {/* Login Form */}
                <form onSubmit={handleSignIn} className="w-100 gap-2 d-flex flex-column">
                    <div className="mb-3">
                        <label className="form-label fw-medium">Email Address</label>
                        <input type="email" name="email" placeholder="name@example.com" className="form-control" 
                            value={formData.email} onChange={handleChange} required
                        />
                    </div>

                    <div className="mb-3">
                        <label className="form-label fw-medium">Password</label>
                        <input type="password" name="password" placeholder="........" className="form-control" 
                            value={formData.password} onChange={handleChange} required
                        />
                    </div>

                    <button type="submit" className="btn eventhub-button w-100" disabled={loading}> 
                        {loading ? "Signing In..." : "Sign In"}
                    </button>

                </form>

                <hr></hr>
                <p className="text-center mt-3">
                    Don't have an account? {" "}
                    <Link to="/register">Sign Up</Link>
                </p>
            </div>
        </div>
    );
}