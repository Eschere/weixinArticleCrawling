window.__resStore = {}

class XHR extends XMLHttpRequest {
    _saveRes(event) {
        const target = event.target
        const {
            responseURL,
            response
        } = target

        const url = new URL(responseURL)
        const store = window.__resStore

        store[url.pathname] = response
    }

    set onload(value) {
        super.onload = (...args) => {
            this._saveRes(...args)
            value.apply(this, args)
        }
    }

    get onload() {
        return super.onload
    }

    set onreadystatechange(value) {
        super.onreadystatechange = (...args) => {
            const target = args[0].target
            if (target.readyState === 4) {
                this._saveRes(...args)
            }

            value.apply(this, args)
        }
    }

    get onreadystatechange() {
        return super.onreadystatechange
    }
}

window.XMLHttpRequest = XHR
