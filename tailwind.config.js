module.exports = {
    theme: {
        extend: {},
    },
    content: [
        'wgui/templates/**/*.jinja2'
    ],
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
    ]
}
