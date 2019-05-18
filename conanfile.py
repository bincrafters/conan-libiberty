# -*- coding: utf-8 -*-
from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class LibibertyConan(ConanFile):
    name = "libiberty"
    version = "9.1.0"
    description = "A collection of subroutines used by various GNU programs"
    topics = ("conan", "libiberty", "gnu", "gnu-collection")
    url = "https://github.com/bincrafters/conan-libiberty"
    homepage = "https://gcc.gnu.org/onlinedocs/libiberty"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "LGPL-2.1"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _libiberty_folder(self):
        return os.path.join("source_subfolder", self.name)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        sha256 = "cc472b9d5ac4c7fdd1dc43c0e1cb00294c658bba29949894cc782506f7cbf149"
        source_url = "https://github.com/gcc-mirror/gcc"
        pkg_version = self.version.replace('.', '_')
        tools.get("{0}/archive/gcc-{1}-release.tar.gz".format(source_url, pkg_version), sha256=sha256)
        extracted_dir = "gcc-gcc-{}-release".format(pkg_version)
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            args = ["--enable-install-libiberty"]
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self._autotools.configure(args=args, configure_dir=self._libiberty_folder)
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        self.copy(pattern="COPYING.LIB", dst="licenses", src=self._libiberty_folder)
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
