module.exports = {
    theme: {
        extend: {},
    },
    content: [
        'wgui/templates/**/*.jinja2',
        "wgui/templates/componetns/flash.jinja2"
    ],
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ]
}
