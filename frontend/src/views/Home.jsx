export function Home() {
    const render = () => {
        return `
            <div class="container">
                <h1>Welcome to the Help Desk</h1>
                <div class="sub-form-container">
                    <p>Please <a href="/login">login</a> or <a href="/register">register</a> to continue.</p>
                </div>
            </div>
        `;
    };

    const addEventListeners = () => {};

    return {
        render,
        addEventListeners
    };
}
