import { useState, useEffect } from "react";
import io from "socket.io-client";
import axios from "axios";

const socket = io("http://localhost:3000");

function App() {
    const [username, setUsername] = useState(""); // Tên user hiện tại
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [users, setUsers] = useState([]); // Danh sách user online

    // Kết nối và gửi username khi user nhập
    useEffect(() => {
        if (username) {
            socket.emit("user_connected", username);

            // Lắng nghe danh sách user online
            socket.on("update_user_list", (onlineUsers) => {
                setUsers(onlineUsers);
            });

            // Lấy tin nhắn mới
            socket.on("receive_message", (newMessage) => {
                setMessages((prev) => [...prev, newMessage]);
            });
        }

        return () => {
            socket.off("update_user_list");
            socket.off("receive_message");
        };
    }, [username]);

    // Lấy lịch sử tin nhắn khi load trang
    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axios.get("http://localhost:3000/messages");
                setMessages(response.data);
            } catch (err) {
                console.error("Error fetching messages:", err);
            }
        };

        fetchMessages();
    }, []);

    // Gửi tin nhắn
    const sendMessage = () => {
        if (message.trim() !== "") {
            socket.emit("send_message", { sender: username, content: message });
            setMessage("");
        }
    };

    return (
        <div>
            {!username ? (
                // Form nhập username
                <div>
                    <h1>Enter your username</h1>
                    <input
                        type="text"
                        placeholder="Your username"
                        onChange={(e) => setUsername(e.target.value)}
                    />
                    <button onClick={() => username && setUsername(username)}>
                        Join Chat
                    </button>
                </div>
            ) : (
                // Giao diện chính của chat
                <div>
                    <h1>Realtime Chat</h1>
                    <h2>Online Users</h2>
                    <ul>
                        {users.map((user, index) => (
                            <li key={index}>{user}</li>
                        ))}
                    </ul>
                    <div>
                        {messages.map((msg, index) => (
                            <p key={index}>
                                <strong>{msg.sender}:</strong> {msg.content}
                            </p>
                        ))}
                    </div>
                    <input
                        type="text"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Type your message"
                    />
                    <button onClick={sendMessage}>Send</button>
                </div>
            )}
        </div>
    );
}

export default App;
