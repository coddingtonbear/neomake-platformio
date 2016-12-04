Neomake-Platformio
==================

Easily configure neomake to recognize your PlatformIO project's include
path.

Installation
------------

1. Install using your favorite Vim plugin manager.
2. Run `UpdateRemotePlugins`.
3. Restart Neovim.

Basic Use
---------

```vimscript
call SetupPlatformioEnvironment('/path/to/your/platformio/project/')
```

Use with Local-vimrc
--------------------

If you use [vim-localvimrc](https://github.com/embear/vim-localvimrc) you
can automatically configure vim when you open a file in a project directory
by doing two things:

1. Adding an ``.lvimrc`` file containing the following line in the same
   level of your project that includes your ``platformio.ini`` file :

   ```vimscript
   call SetupPlatformioEnvironment(expand('<sfile>:p'))
   ```
2. Disabling lvimrc sandboxing by setting the following setting in your
   ``~/.config/nvim/init.vim``:

   ```vimscript
   let g:localvimrc_sandbox = 0
   ```

Note that if you work on third-party projects, any code in those projects'
``.lvimrc`` files include could be executed outside the sandbox; if you
disable the sandbox as described above, be sure to carefully examine the
contents of unfamiliar paths when localvimrc asks you whether you'd like
to source a new localvimrc configuration file!


